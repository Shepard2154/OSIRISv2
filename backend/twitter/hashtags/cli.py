import argparse
import collections
import contextlib
import dataclasses
import datetime
import os
import importlib.metadata
import inspect
import logging
import time
import requests
import multiprocessing as mp
import sys
import tempfile
import twitter
import json
import pandas as pd
import loguru


dumpLocals = False
logger = logging


class Logger(logging.Logger):
	def _log_with_stack(self, level, *args, **kwargs):
		super().log(level, *args, **kwargs)
		if dumpLocals:
			stack = inspect.stack()
			if len(stack) >= 3:
				name = _dump_stack_and_locals(stack[2:][::-1])
				super().log(level, f'Dumped stack and locals to {name}')

	def warning(self, *args, **kwargs):
		self._log_with_stack(logging.WARNING, *args, **kwargs)

	def error(self, *args, **kwargs):
		self._log_with_stack(logging.ERROR, *args, **kwargs)

	def critical(self, *args, **kwargs):
		self._log_with_stack(logging.CRITICAL, *args, **kwargs) 

	def log(self, level, *args, **kwargs):
		if level >= logging.WARNING:
			self._log_with_stack(level, *args, **kwargs)
		else:
			super().log(level, *args, **kwargs)


def _requests_request_repr(name, request):
	ret = []
	ret.append(f'{name} = {request!r}')
	ret.append(f'\n  {name}.method = {request.method}')
	ret.append(f'\n  {name}.url = {request.url}')
	ret.append(f'\n  {name}.headers = \\')
	for field in request.headers:
		ret.append(f'\n    {field} = {_repr("_", request.headers[field])}')
	for attr in ('body', 'params', 'data'):
		if hasattr(request, attr) and getattr(request, attr):
			ret.append(f'\n  {name}.{attr} = ')
			ret.append(_repr('_', getattr(request, attr)).replace('\n', '\n  '))
	return ''.join(ret)


def _requests_response_repr(name, response, withHistory = True):
	ret = []
	ret.append(f'{name} = {response!r}')
	ret.append(f'\n  {name}.url = {response.url}')
	ret.append(f'\n  {name}.request = ')
	ret.append(_repr('_', response.request).replace('\n', '\n  '))
	if withHistory and response.history:
		ret.append(f'\n  {name}.history = [')
		for previousResponse in response.history:
			ret.append(f'\n    ')
			ret.append(_requests_response_repr('_', previousResponse, withHistory = False).replace('\n', '\n    '))
		ret.append('\n  ]')
	ret.append(f'\n  {name}.status_code = {response.status_code}')
	ret.append(f'\n  {name}.headers = \\')
	for field in response.headers:
		ret.append(f'\n    {field} = {_repr("_", response.headers[field])}')
	ret.append(f'\n  {name}.content = {_repr("_", response.content)}')
	return ''.join(ret)


def _requests_exception_repr(name, exc):
	ret = []
	ret.append(f'{name} = {exc!r}')
	ret.append(f'\n  ' + _repr(f'{name}.request', exc.request).replace('\n', '\n  '))
	ret.append(f'\n  ' + _repr(f'{name}.response', exc.response).replace('\n', '\n  '))
	return ''.join(ret)


def _repr(name, value):
	if type(value) is requests.Response:
		return _requests_response_repr(name, value)
	if type(value) in (requests.PreparedRequest, requests.Request):
		return _requests_request_repr(name, value)
	if isinstance(value, requests.exceptions.RequestException):
		return _requests_exception_repr(name, value)
	if isinstance(value, dict):
		return f'{name} = <{type(value).__module__}.{type(value).__name__}>\n  ' + \
		       '\n  '.join(_repr(f'{name}[{k!r}]', v).replace('\n', '\n  ') for k, v in value.items())
	if isinstance(value, (list, tuple, collections.deque)) and not all(isinstance(v, (int, str)) for v in value):
		return f'{name} = <{type(value).__module__}.{type(value).__name__}>\n  ' + \
		       '\n  '.join(_repr(f'{name}[{i}]', v).replace('\n', '\n  ') for i, v in enumerate(value))
	if dataclasses.is_dataclass(value) and not isinstance(value, type):
		return f'{name} = <{type(value).__module__}.{type(value).__name__}>\n  ' + \
		       '\n  '.join(_repr(f'{name}.{f.name}', f.name) + ' = ' + _repr(f'{name}.{f.name}', getattr(value, f.name)).replace('\n', '\n  ') for f in dataclasses.fields(value))
	valueRepr = f'{name} = {value!r}'
	if '\n' in valueRepr:
		return ''.join(['\\\n  ', valueRepr.replace('\n', '\n  ')])
	return valueRepr


@contextlib.contextmanager
def _dump_locals_on_exception():
	try:
		yield
	except Exception as e:
		trace = inspect.trace()
		if len(trace) >= 2:
			name = _dump_stack_and_locals(trace[1:], exc = e)
			logger.fatal(f'Dumped stack and locals to {name}')
		raise


def _dump_stack_and_locals(trace, exc = None):
	with tempfile.NamedTemporaryFile('w', prefix = 'snscrape_locals_', delete = False) as fp:
		if exc is not None:
			fp.write('Exception:\n')
			fp.write(f'  {type(exc).__module__}.{type(exc).__name__}: {exc!s}\n')
			fp.write(f'  args: {exc.args!r}\n')
			fp.write('\n')

		fp.write('Stack:\n')
		for frameRecord in trace:
			fp.write(f'  File "{frameRecord.filename}", line {frameRecord.lineno}, in {frameRecord.function}\n')
			for line in frameRecord.code_context:
				fp.write(f'    {line.strip()}\n')
		fp.write('\n')

		for frameRecord in trace:
			module = inspect.getmodule(frameRecord[0])
			if not module.__name__.startswith('snscrape.') and module.__name__ != 'snscrape':
				continue
			locals_ = frameRecord[0].f_locals
			fp.write(f'Locals from file "{frameRecord.filename}", line {frameRecord.lineno}, in {frameRecord.function}:\n')
			for variableName in locals_:
				variable = locals_[variableName]
				varRepr = _repr(variableName, variable)
				fp.write(f'  {variableName} {type(variable)} = ')
				fp.write(varRepr.replace('\n', '\n  '))
				fp.write('\n')
			fp.write('\n')
			if 'self' in locals_ and hasattr(locals_['self'], '__dict__'):
				fp.write(f'Object dict:\n')
				fp.write(repr(locals_['self'].__dict__))
				fp.write('\n\n')
		name = fp.name
	return name


def parse_datetime_arg(arg):
	for format in ('%Y-%m-%d %H:%M:%S %z', '%Y-%m-%d %H:%M:%S', '%Y-%m-%d %z', '%Y-%m-%d'):
		try:
			d = datetime.datetime.strptime(arg, format)
		except ValueError:
			continue
		else:
			if d.tzinfo is None:
				return d.replace(tzinfo = datetime.timezone.utc)
			return d
	# Try treating it as a unix timestamp
	try:
		d = datetime.datetime.fromtimestamp(int(arg), datetime.timezone.utc)
	except ValueError:
		pass
	else:
		return d
	raise argparse.ArgumentTypeError(f'Cannot parse {arg!r} into a datetime object')


def parse_format(arg):
	# Replace '{' by '{0.' to use properties of the item, but keep '{{' intact
	parts = arg.split('{')
	out = ''
	it = iter(zip(parts, parts[1:]))
	for part, nextPart in it:
		out += part
		if nextPart == '': # Double brace
			out += '{{'
			next(it)
		else: # Single brace
			out += '{0.'
	out += parts[-1]
	return out


def setup_logging():
	logging.setLoggerClass(Logger)
	global logger
	logger = logging.getLogger(__name__)


def configure_logging(verbosity, dumpLocals_):
	global dumpLocals
	dumpLocals = dumpLocals_

	rootLogger = logging.getLogger()

	# Set level
	if verbosity > 0:
		level = logging.INFO if verbosity == 1 else logging.DEBUG
		rootLogger.setLevel(level)
		for handler in rootLogger.handlers:
			handler.setLevel(level)

	# Create formatter
	formatter = logging.Formatter('{asctime}.{msecs:03.0f}  {levelname}  {name}  {message}', datefmt = '%Y-%m-%d %H:%M:%S', style = '{')

	# Remove existing handlers
	for handler in rootLogger.handlers:
		rootLogger.removeHandler(handler)

	# Add stream handler
	handler = logging.StreamHandler()
	handler.setFormatter(formatter)
	rootLogger.addHandler(handler)


def download_tweets(hashtag_item):
	scraper = twitter.TwitterHashtagScraper(hashtag_item)

	tweets = []
	for tweet in scraper.get_items():
		tweets.append(json.loads(tweet.json()))
		break

	return tweets

@loguru.logger.catch
def main():
	hashtags = ['#ринапаленкова', '#навальный', '#ворывзаконе', '#ультрас', '#цсканавыезде', '#коррупция', '#суицидница', '#анархосиндикализм', '#суицидальноенастроение', '#жалостьксебе', '#АУЕ', '#печаль', '#стоник', '#фксм', '#алексейнавальный', '#хочусдохнуть', '#добив', '#дракадевушек', '#диланклиболт', '#свободныевыборы', '#эрикхаррис', '#ворамсвободу', '#россиябезпутина', '#анархо_синдикализм', '#депрессия', '#забив', '#офвайны', '#путинуходи', '#путинавотставку', '#одиночество', '#обнуление', '#диланклиболд', '#мыждемперемен', '#зенитнавыезде', '#боль', '#томастиджейлейн', '#суицид', '#околофутбола', '#ФанатыСпартака', '#футбольныехулиганы', '#противпутина', '#обнулёныш', '#забивы', '#керченскийстрелок', '#воры', '#вставайроссия', '#забивной', '#чиновники', '#спартакнавыезде', '#офник', '#анархопримитивизм', '#antisystem', '#акаб', '#navalny', '#шакромолодой', '#свободуфургалу', '#мусорабляпидорасы', '#фартумасти', '#ильназбог', '#анархия', '#смертьмусорам', '#черныйдельфин', '#разбитоесердце', '#тимурбекманнсуров', '#доляворовская', '#блатнойжаргон', '#россиябудетсвободной', '#влалиславросляков', '#хватиттерпеть', '#свободунавальному', '#freenavalny', '#диланруф', '#безысходность', '#фанатнепреступник', '#хватит_молчать', '#няпока', '#забивыоф', '#самоубийство', '#скулшутер', '#оукб', '#суицидвыход', '#фанатыцска', '#анархокомунизм', '#розбитоесерце', '#криминальнаяроссия', '#ауежизньворам', '#расходыначиновников', '#протест', '#воровскойзакон', '#владросляков', '#суицыд', '#ericharris1999', '#anarchism', '#сбг', '#казанскийстрелок', '#ямыфургал', '#путинврагроссии', '#дедхасан', '#анархофеменизм', '#schoolshoooter', '#селфхарм', '#anarchy', '#скулшутеры', '#офф', '#тревога', '#свободуполитзаключенным', '#саморазрушение', '#краснобелые', '#едровведро', '#разбитаядуша', '#дзенанархия', '#митинг', '#галявиевильназ', '#ворвзаконе', '#криминал', '#блатной', '#бекмансуров', '#жизньворам', '#сашасевер', '#dylankleblold', '#венывскрыты', '#фклм', '#криминальныймир', '#долойпутина', '#путинвор', '#офники', '#стадионнетюрьма', '#колумбайн', '#путинлжец', '#анархизм', '#сэлфхарм', '#офзабивы']
	# save_tweets('#ринапаленкова')

	# pool = mp.Pool(len(os.sched_getaffinity(0)))
	# pool.map(save_tweets, new_hashtags)


if __name__ == "__main__":
	main()