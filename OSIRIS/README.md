# OSIRISv2.1

## Примеры POST - запросов:

## /special/v2/hashtags/
`{
    "values": ["ole", "xsd"],
    "mode_flag": 1
}`

## /special/v2/hashtags/
`{
    "all_flag": true,
    "mode_flag": 1
}`

## /special/monitoring/hashtags/
`{
    "values": ["ole", "xsd"],
    "all_flag": false,
    "mode_flag": 1,
    "interval": 10 
}`

## /special/monitoring/persons/
`{
    "values": ["confusedlexa", "JoeBiden"],
    "all_flag": false,
    "mode_flag": 1,
    "interval": 10 
}`

## /special/monitoring/persons/
`{
    "all_flag": true,
    "mode_flag": 1,
    "interval": 10 
}`