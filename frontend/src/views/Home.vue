<template>
  <div class="small">
    <v-row
    justify-content="space-around"
    > 
    <v-text-field
      id="screen_name_field"
      label="Введите псевдоним пользователя"
      placeholder="JoeBiden"
      v-model="username"
      :append-outer-icon="username ? 'mdi-account-search' : ''"
      @click:append-outer="download()"
      clearable
      outlined
    ></v-text-field>
    </v-row>

    <v-row>
      <v-col>
        <v-card 
        class="card_info"
        elevation="5">
          <v-row>
            <v-col>
              <v-img
                lazy-src="https://picsum.photos/id/11/10/6"
                max-height="150"
                max-width="150"
                src="https://picsum.photos/id/11/500/300"
              ></v-img>
            </v-col>

            <v-col>
              <p id="username">Oleg Burnaev</p>
              <p id="screen_name">@olegburn</p>
            </v-col>
          </v-row>

          <v-row>
            <v-col>
              <div class="stat_item">
                  <p class="stat_number">123</p>
                  <p class="stat_caption">Твиты</p>
              </div>
              <div class="stat_item">
                  <p class="stat_number">123</p>
                  <p class="stat_caption">Подписки</p>
              </div>
            </v-col>

            <v-col>
              <div class="stat_item">
                  <p class="stat_number">123</p>
                  <p class="stat_caption">Лайки</p>
              </div>
              <div class="stat_item">
                  <p class="stat_number">123</p>
                  <p class="stat_caption">Списки</p>
              </div>
            </v-col>

            <v-col>
              <div class="stat_item">
                  <p class="stat_number">123</p>
                  <p class="stat_caption">Подписчики</p>
              </div>
            </v-col>
          </v-row>

          <p><v-icon>mdi-file-account-outline</v-icon> Husband to @DrBiden, proud father and grandfather. Ready to build back better for all Americans. Official account is @POTUS.</p>
          <p id="created_at"><v-icon>mdi-calendar-edit</v-icon>2022</p>
          <p id="person_id"><v-icon>mdi-account-key</v-icon>12321421434</p>
          <p id="person_url"><v-icon>mdi-web</v-icon> http://vk.com/</p>
          <p id="location"><v-icon>mdi-map-marker</v-icon> New York</p>
        </v-card>
      </v-col>

      <v-col>
        <v-card
        class="card_info"
        elevation="5">
          <VueApexCharts width="500" type="heatmap" :options="options" :series="series"></VueApexCharts>
        </v-card>
      </v-col>
    </v-row>

    <v-row>
      <v-col>
        <v-card
          class="card_info"
          elevation="5">
            <VueApexCharts width="500" type="line" :options="lineoptions" :series="lineseries"></VueApexCharts>
        </v-card>
      </v-col>

      <v-col>
        <v-card
          class="card_info"
          elevation="5">
            <VueApexCharts width="500" type="pie" :options="pieoptions" :series="pieseries"></VueApexCharts>
        </v-card>
      </v-col>
    </v-row>

    <v-row>
      <v-col>
        <v-card
        class="card_info"
        elevation="5">
          <VueApexCharts type="bar" :options="typeTweetOptions" :series="typeTweetSeries"></VueApexCharts>
      </v-card>
      </v-col>

      <v-col>
        <v-card
        class="card_info"
        elevation="5">
          <VueApexCharts type="bar" :options="langTweetOptions" :series="langTweetSeries"></VueApexCharts>
        </v-card>
      </v-col>

      <v-col>
        <v-card
        class="card_info"
        elevation="5">
          <VueApexCharts type="bar" :options="clientTweetOptions" :series="clientTweetSeries"></VueApexCharts>
      </v-card>
      </v-col>
    </v-row>

    <v-row>
      <v-col>
        <v-card
        class="card_info"
        elevation="5">
          <VueApexCharts type="bar" :options="hashtagsTweetOptions" :series="hashtagsTweetSeries"></VueApexCharts>
        </v-card>
      </v-col>
      
      <v-col>
        <v-card
        class="card_info"
        elevation="5">
          <VueApexCharts type="bar" :options="urlsTweetOptions" :series="urlsTweetSeries"></VueApexCharts>
        </v-card>
      </v-col>
    </v-row>

    <v-row>
      <v-col>
        <v-card
        class="card_info"
        elevation="5">
          <VueApexCharts type="bar" :options="quotesTweetOptions" :series="quotesTweetSeries"></VueApexCharts>
        </v-card>
      </v-col>
      <v-col>
        <v-card
        class="card_info"
        elevation="5">
          <VueApexCharts type="bar" :options="retweetsTweetOptions" :series="retweetsTweetSeries"></VueApexCharts>
        </v-card>
      </v-col>
      <v-col>
        <v-card
        class="card_info"
        elevation="5">
          <VueApexCharts type="bar" :options="usersTweetOptions" :series="usersTweetSeries"></VueApexCharts>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script>
  import LineChart from '../components/LineChart'
  import VueApexCharts from 'vue-apexcharts'


  export default {
    components: {
      LineChart,
      VueApexCharts
    },

    data() {
      return {
        username: '',
        options: {
          noData: {
              text: 'Не найдено...'
          },
          chart: {
              id:"chartheatmap",
              height: 350,
              type: 'heatmap',
          },
          xaxis: {
              type: 'category',
              categories: ["00:00", "01:00", "02:00", "03:00", "04:00", "05:00", "06:00", "07:00", "08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00", "21:00", "22:00", "23:00"]
          },
          dataLabels: {
              enabled: false
          },
          colors: ["#008FFB"],
          title: {
              text: 'Активность публикаций'
            }
        },
        series: [
          {
              name: 'Вск',
              data: [26, 25, 14, 4, 3, 0, 0, 0, 0, 0, 0, 1, 6, 9, 22, 28, 30, 27, 28, 26, 33, 33, 31, 32]
          },
          {
              name: 'Сб',
              data: [31, 13, 6, 4, 3, 2, 0, 0, 0, 0, 0, 1, 6, 9, 36, 30, 31, 33, 32, 24, 42, 35, 25, 38]
          },
          {
              name: 'Пт',
              data: [43, 49, 26, 20, 7, 6, 4, 1, 0, 0, 1, 3, 3, 13, 25, 32, 26, 39, 52, 38, 46, 42, 35, 48]
          },
          {
              name: 'Чт',
              data: [49, 33, 37, 11, 1, 3, 1, 0, 0, 0, 0, 2, 3, 15, 31, 29, 28, 25, 43, 34, 29, 55, 31, 42]
          },
          {
              name: 'Ср',
              data: [44, 51, 34, 10, 0, 0, 2, 0, 0, 0, 0, 1, 3, 8, 29, 22, 38, 34, 33, 37, 45, 48, 30, 42]
          },
          {
              name: 'Вт',
              data: [52, 56, 38, 15, 4, 0, 0, 0, 0, 0, 0, 4, 4, 11, 20, 39, 23, 38, 29, 35, 33, 36, 34, 35]
          },
          {
              name: 'Пн',
              data: [31, 22, 6, 8, 4, 0, 0, 0, 0, 0, 0, 2, 3, 11, 31, 25, 36, 33, 27, 30, 27, 27, 35, 35]
          }
        ],
        lineoptions: {
          noData: {
              text: 'Не найдено...'
          },
          chart: {
              id:"chartt",
              height: 350,
              type: 'area',
          },

          dataLabels: {
              enabled: false
          },
          stroke: {
              width: 2
          },

          grid: {
              row: {
                  colors: ['#fff', "#f2f2f2"]
              }
          },
          xaxis: {
              labels: {
                  rotate: -45
              },
              categories: ['2020-04-23', '2020-04-24', '2020-04-25', '2020-04-26', '2020-04-27', '2020-04-28', '2020-04-29', '2020-04-30', '2020-05-01', '2020-05-02', '2020-05-03', '2020-05-04', '2020-05-05', '2020-05-06', '2020-05-07', '2020-05-08', '2020-05-09', '2020-05-10', '2020-05-11', '2020-05-12', '2020-05-13', '2020-05-14', '2020-05-15', '2020-05-16', '2020-05-17', '2020-05-18', '2020-05-19', '2020-05-20', '2020-05-21', '2020-05-22', '2020-05-23', '2020-05-24', '2020-05-25', '2020-05-26', '2020-05-27', '2020-05-28', '2020-05-29', '2020-05-30', '2020-05-31', '2020-06-01', '2020-06-02', '2020-06-03', '2020-06-04', '2020-06-05', '2020-06-06', '2020-06-07', '2020-06-08', '2020-06-09', '2020-06-10', '2020-06-11', '2020-06-12', '2020-06-13', '2020-06-14', '2020-06-15', '2020-06-16', '2020-06-17', '2020-06-18', '2020-06-19', '2020-06-20', '2020-06-21', '2020-06-22', '2020-06-23', '2020-06-24', '2020-06-25', '2020-06-26', '2020-06-27', '2020-06-28', '2020-06-29', '2020-06-30', '2020-07-01', '2020-07-02', '2020-07-03', '2020-07-04', '2020-07-05', '2020-07-06', '2020-07-07', '2020-07-08', '2020-07-09', '2020-07-10', '2020-07-11', '2020-07-12', '2020-07-13', '2020-07-14', '2020-07-15', '2020-07-16', '2020-07-17', '2020-07-18', '2020-07-19', '2020-07-20', '2020-07-21', '2020-07-22', '2020-07-23', '2020-07-24', '2020-07-25', '2020-07-26', '2020-07-27', '2020-07-28', '2020-07-29', '2020-07-30', '2020-07-31', '2020-08-01', '2020-08-02', '2020-08-03', '2020-08-04', '2020-08-05', '2020-08-06', '2020-08-07', '2020-08-08', '2020-08-09', '2020-08-10', '2020-08-11', '2020-08-12', '2020-08-13', '2020-08-14', '2020-08-15', '2020-08-16', '2020-08-17', '2020-08-18', '2020-08-19', '2020-08-20', '2020-08-21', '2020-08-22', '2020-08-23', '2020-08-24', '2020-08-25', '2020-08-26', '2020-08-27', '2020-08-28', '2020-08-29', '2020-08-30', '2020-08-31', '2020-09-01', '2020-09-02', '2020-09-03', '2020-09-04', '2020-09-05', '2020-09-06', '2020-09-07', '2020-09-08', '2020-09-09', '2020-09-10', '2020-09-11', '2020-09-12', '2020-09-13', '2020-09-14', '2020-09-15', '2020-09-16', '2020-09-17', '2020-09-18', '2020-09-19', '2020-09-20', '2020-09-21', '2020-09-22', '2020-09-23', '2020-09-24', '2020-09-25', '2020-09-26', '2020-09-27', '2020-09-28', '2020-09-29', '2020-09-30', '2020-10-01', '2020-10-02', '2020-10-03', '2020-10-04', '2020-10-05', '2020-10-06', '2020-10-07', '2020-10-08', '2020-10-09', '2020-10-10', '2020-10-11', '2020-10-12', '2020-10-13', '2020-10-14', '2020-10-15', '2020-10-16', '2020-10-17', '2020-10-18', '2020-10-19', '2020-10-20', '2020-10-21', '2020-10-22', '2020-10-23', '2020-10-24', '2020-10-25', '2020-10-26', '2020-10-27', '2020-10-28', '2020-10-29', '2020-10-30', '2020-10-31', '2020-11-01', '2020-11-02', '2020-11-03', '2020-11-04', '2020-11-05', '2020-11-06', '2020-11-07', '2020-11-08', '2020-11-09', '2020-11-10', '2020-11-11', '2020-11-12', '2020-11-13', '2020-11-14', '2020-11-15', '2020-11-16', '2020-11-17', '2020-11-18', '2020-11-19', '2020-11-20', '2020-11-21', '2020-11-23', '2020-11-24', '2020-11-25', '2020-11-26', '2020-11-27', '2020-11-28', '2020-11-29', '2020-11-30', '2020-12-01', '2020-12-02', '2020-12-03', '2020-12-04', '2020-12-05', '2020-12-06', '2020-12-07', '2020-12-08', '2020-12-09', '2020-12-10', '2020-12-11', '2020-12-12', '2020-12-13', '2020-12-14', '2020-12-15', '2020-12-16', '2020-12-17', '2020-12-18', '2020-12-19', '2020-12-20', '2020-12-21', '2020-12-22', '2020-12-23', '2020-12-24', '2020-12-25', '2020-12-26', '2020-12-27', '2020-12-28', '2020-12-29', '2020-12-30', '2020-12-31', '2021-01-01', '2021-01-02', '2021-01-03', '2021-01-04', '2021-01-05', '2021-01-06', '2021-01-07', '2021-01-08', '2021-01-09', '2021-01-10', '2021-01-11', '2021-01-12', '2021-01-13', '2021-01-14', '2021-01-15', '2021-01-16', '2021-01-17', '2021-01-18', '2021-01-19', '2021-01-20', '2021-01-21', '2021-01-22', '2021-01-23', '2021-01-24', '2021-01-27', '2021-01-31', '2021-02-01', '2021-02-02', '2021-02-03', '2021-02-04', '2021-02-05', '2021-02-06', '2021-02-07', '2021-02-08', '2021-02-09', '2021-02-10', '2021-02-11', '2021-02-12', '2021-02-13', '2021-02-14', '2021-02-16', '2021-02-17', '2021-02-18', '2021-02-19', '2021-02-20', '2021-02-21', '2021-02-22', '2021-02-23', '2021-02-24', '2021-02-25', '2021-02-26', '2021-02-27', '2021-02-28', '2021-03-01', '2021-03-02', '2021-03-03', '2021-03-04', '2021-03-05', '2021-03-06', '2021-03-07', '2021-03-08', '2021-03-09', '2021-03-10', '2021-03-11', '2021-03-12', '2021-03-13', '2021-03-14', '2021-03-15', '2021-03-16', '2021-03-18', '2021-03-19', '2021-03-20', '2021-03-21', '2021-03-22', '2021-03-23', '2021-03-24', '2021-03-25', '2021-03-26', '2021-03-27', '2021-03-28', '2021-03-29', '2021-03-30', '2021-03-31', '2021-04-01', '2021-04-03', '2021-04-04', '2021-04-05', '2021-04-06', '2021-04-07', '2021-04-08', '2021-04-09', '2021-04-10', '2021-04-12', '2021-04-13', '2021-04-14', '2021-04-16', '2021-04-18', '2021-04-19', '2021-04-20', '2021-04-21', '2021-04-22', '2021-04-23', '2021-04-24', '2021-04-25', '2021-04-26', '2021-04-27', '2021-04-28', '2021-04-29', '2021-04-30', '2021-05-01', '2021-05-02', '2021-05-03', '2021-05-04', '2021-05-05', '2021-05-06', '2021-05-07', '2021-05-08', '2021-05-09', '2021-05-10', '2021-05-11', '2021-05-12', '2021-05-13', '2021-05-14', '2021-05-15', '2021-05-17', '2021-05-18', '2021-05-19', '2021-05-20', '2021-05-21', '2021-05-22', '2021-05-23', '2021-05-24', '2021-05-25', '2021-05-26', '2021-05-27', '2021-05-28', '2021-05-29', '2021-05-31', '2021-06-01', '2021-06-02', '2021-06-03', '2021-06-04', '2021-06-05', '2021-06-06', '2021-06-07', '2021-06-08', '2021-06-09', '2021-06-10', '2021-06-11', '2021-06-12', '2021-06-13', '2021-06-14', '2021-06-15', '2021-06-16', '2021-06-17', '2021-06-18', '2021-06-19', '2021-06-20', '2021-06-21', '2021-06-22', '2021-06-23', '2021-06-24', '2021-06-26', '2021-06-29', '2021-06-30', '2021-07-01', '2021-07-02', '2021-07-03', '2021-07-04', '2021-07-06', '2021-07-07', '2021-07-08', '2021-07-09', '2021-07-11', '2021-07-14', '2021-07-15', '2021-07-16', '2021-07-17', '2021-07-18', '2021-07-19', '2021-07-20', '2021-07-22', '2021-07-23', '2021-07-24', '2021-07-25', '2021-07-26', '2021-07-27', '2021-07-29', '2021-07-31', '2021-08-01', '2021-08-02', '2021-08-03', '2021-08-04', '2021-08-05', '2021-08-06', '2021-08-07', '2021-08-09', '2021-08-10', '2021-08-11', '2021-08-12', '2021-08-13', '2021-08-14', '2021-08-16', '2021-08-17', '2021-08-18', '2021-08-22', '2021-08-23', '2021-08-24', '2021-08-25', '2021-08-27', '2021-08-28', '2021-08-29', '2021-08-31', '2021-09-01', '2021-09-02', '2021-09-03', '2021-09-04', '2021-09-06', '2021-09-08', '2021-09-09', '2021-09-10', '2021-09-11', '2021-09-12', '2021-09-14', '2021-09-15', '2021-09-16', '2021-09-17', '2021-09-18', '2021-09-19', '2021-09-20', '2021-09-21', '2021-09-22', '2021-09-23', '2021-09-24', '2021-09-25', '2021-09-26', '2021-09-27', '2021-09-28', '2021-09-29', '2021-09-30', '2021-10-01', '2021-10-02', '2021-10-05', '2021-10-06', '2021-10-07', '2021-10-08', '2021-10-09', '2021-10-10', '2021-10-12', '2021-10-13', '2021-10-14', '2021-10-15', '2021-10-16', '2021-10-17', '2021-10-18', '2021-10-19', '2021-10-20', '2021-10-22', '2021-10-23', '2021-10-24', '2021-10-25', '2021-10-26', '2021-10-27', '2021-10-28', '2021-10-29', '2021-10-30', '2021-10-31', '2021-11-01', '2021-11-02', '2021-11-04', '2021-11-05', '2021-11-06', '2021-11-07', '2021-11-08', '2021-11-09', '2021-11-10', '2021-11-11', '2021-11-12', '2021-11-13', '2021-11-14', '2021-11-15', '2021-11-16', '2021-11-17', '2021-11-18', '2021-11-19', '2021-11-20', '2021-11-21', '2021-11-22', '2021-11-23', '2021-11-24', '2021-11-25', '2021-11-26', '2021-11-27'],
              tickPlacement: 'on'
          },
          yaxis: {
              title: {
                  text: '',
              },
          },
          fill: {
              type: 'gradient',
              gradient: {
                  shade: 'light',
                  type: "vertical",
                  shadeIntensity: 0.25,
                  gradientToColors: undefined,
                  inverseColors: true,
              },
          }
        },
        lineseries: [{
        name: 'Число твитов',
        data: [3, 10, 18, 6, 9, 9, 9, 9, 10, 8, 10, 7, 6, 11, 9, 12, 7, 7, 9, 8, 8, 13, 11, 7, 8, 7, 8, 12, 9, 12, 7, 9, 3, 6, 12, 7, 9, 6, 2, 3, 10, 7, 9, 11, 9, 6, 5, 10, 7, 11, 8, 7, 5, 6, 9, 6, 10, 9, 7, 5, 7, 8, 8, 8, 6, 7, 5, 7, 7, 8, 8, 7, 5, 7, 5, 8, 7, 11, 6, 8, 7, 7, 8, 6, 5, 8, 4, 6, 7, 10, 9, 9, 6, 7, 7, 7, 15, 9, 9, 8, 6, 6, 7, 12, 9, 8, 13, 8, 9, 6, 8, 17, 9, 10, 7, 8, 7, 32, 20, 26, 22, 8, 6, 3, 9, 12, 13, 25, 9, 7, 16, 15, 9, 8, 9, 5, 6, 9, 9, 15, 9, 8, 6, 9, 8, 12, 11, 13, 22, 6, 10, 4, 11, 7, 13, 7, 10, 8, 9, 11, 42, 15, 8, 8, 7, 13, 36, 20, 35, 18, 13, 10, 15, 17, 15, 22, 26, 13, 14, 12, 20, 15, 15, 42, 20, 18, 18, 16, 20, 23, 18, 32, 49, 53, 54, 22, 13, 3, 9, 16, 8, 7, 4, 4, 2, 3, 1, 7, 3, 2, 3, 7, 2, 3, 9, 9, 5, 4, 3, 4, 4, 8, 7, 6, 7, 5, 3, 6, 7, 7, 9, 6, 6, 6, 8, 10, 6, 6, 3, 3, 6, 4, 5, 7, 8, 1, 1, 3, 3, 7, 6, 4, 4, 2, 3, 5, 9, 8, 7, 8, 3, 3, 5, 4, 2, 3, 6, 4, 5, 3, 6, 8, 3, 2, 5, 2, 1, 1, 1, 2, 2, 3, 2, 1, 2, 2, 3, 1, 3, 2, 2, 2, 2, 3, 3, 2, 2, 2, 2, 3, 2, 2, 3, 1, 2, 2, 4, 2, 1, 1, 2, 1, 2, 2, 3, 1, 3, 2, 2, 2, 2, 2, 3, 1, 2, 2, 1, 2, 2, 2, 1, 1, 2, 1, 4, 3, 1, 1, 1, 2, 1, 2, 1, 1, 1, 2, 3, 2, 1, 1, 3, 1, 2, 1, 2, 2, 2, 2, 2, 6, 2, 4, 1, 2, 1, 1, 1, 2, 2, 2, 1, 2, 2, 7, 1, 1, 2, 4, 1, 3, 1, 1, 2, 3, 2, 2, 2, 4, 1, 2, 1, 3, 3, 3, 3, 2, 1, 2, 2, 3, 1, 2, 1, 2, 3, 2, 2, 1, 1, 1, 2, 1, 2, 2, 2, 1, 1, 2, 2, 1, 1, 1, 1, 1, 2, 1, 2, 2, 1, 2, 2, 2, 1, 1, 1, 1, 1, 2, 1, 1, 2, 2, 1, 1, 1, 1, 4, 2, 1, 1, 2, 1, 2, 3, 2, 2, 3, 1, 2, 2, 2, 1, 1, 1, 1, 4, 3, 1, 1, 1, 3, 2, 3, 4, 2, 5, 1, 3, 5, 2, 1, 2, 5, 3, 2, 2, 4, 6, 5, 4, 3, 1, 3, 2, 3, 2, 4, 3, 4, 3, 2, 1, 2, 3, 5, 3, 3, 1, 1, 5, 4, 3, 3, 5, 2, 7, 6, 4, 2, 1, 5, 5, 5, 5, 7, 7, 3, 4, 3, 2, 4, 2, 6, 7, 2, 5, 2, 3, 3, 3, 4, 3, 2, 2, 2]
        }],
        pieoptions: {
          noData: {
              text: 'Не найдено...'
          },
          chart: {
              width: '100%',
              type: 'pie',
          },
          labels: ["Воскресенье", "Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"],
          theme: {
              monochrome: {
                  enabled: true
              }
          },
          title: {
              text: "Число публикаций по дням недели"
          },
          responsive: [{
              breakpoint: 480,
              options: {
                  chart: {
                      width: 200
                  },
                  legend: {
                      position: 'bottom'
                  }
              }
          }]
        },
        pieseries: [378, 401, 559, 504, 512, 506, 393],
        langTweetOptions: {
          noData: {
              text: 'Не найдено...'
          },
          chart: {
              id:"chartTypeTwit",
              type: 'bar',
              height: 300
          },
          plotOptions: {
              bar: {
                  horizontal: true
              }
          },

          dataLabels: {
              enabled: true,
              textAnchor: 'start',
              style: {
                  colors: ['#fff']
              },
              formatter: function (val, opt) {
                  return opt.w.globals.labels[opt.dataPointIndex] + ":  " + val
              },
              offsetX: 0,
              dropShadow: {
                  enabled: true,
                  top: 0,
                  left: 0,
                  blur: 1,
                  opacity: 4.5
              }
          },
          yaxis: {
              labels: {
                  show: false
              }
          },
          xaxis: {
              categories: ['Ретвиты', 'Цитаты', 'Твиты/Ответы'],
              labels: {
                  show: false
              }
          }

        },
        typeTweetSeries: [{
        name: "Количество",
        data: [42008246, 239, 3250]
        }],
        typeTweetOptions: {
          noData: {
              text: 'Не найдено...'
          },
          chart: {
        id:"chartLang",
        type: 'bar',
        height: 300
    },
    plotOptions: {
        bar: {
            horizontal: true,
        }
    },

    dataLabels: {
        enabled: true,
        textAnchor: 'start',
        style: {
            colors: ['#fff']
        },
        formatter: function (val, opt) {
            return opt.w.globals.labels[opt.dataPointIndex] + ":  " + val
        },
        offsetX: 0,
        dropShadow: {
            enabled: true,
            top: 0,
            left: 0,
            blur: 1,
            opacity: 4.5
        }
        },
        yaxis: {
            labels: {
                show: false
            }
        },
        xaxis: {
            categories: ['en', 'es', 'und', 'fr', 'pt', 'tr'],
            labels: {
                show: false
            }
        }

        },
        langTweetSeries: [{
          name: "Количество",
          data: [3216, 21, 9, 2, 1, 1]
        }],
        clientTweetOptions: {
          noData: {
              text: 'Не найдено...'
          },
          chart: {
        id:"chartLang",
        type: 'bar',
        height: 300
    },
    plotOptions: {
        bar: {
            horizontal: true,
        }
    },

    dataLabels: {
        enabled: true,
        textAnchor: 'start',
        style: {
            colors: ['#fff']
        },
        formatter: function (val, opt) {
            return opt.w.globals.labels[opt.dataPointIndex] + ":  " + val
        },
        offsetX: 0,
        dropShadow: {
            enabled: true,
            top: 0,
            left: 0,
            blur: 1,
            opacity: 4.5
        }
        },
        yaxis: {
            labels: {
                show: false
            }
        },
        xaxis: {
            categories: ['TweetDeck', 'Twitter Web App', 'Twitter Media Studio', 'Sprout Social', 'Periscope', 'Twitter for iPhone'],
            labels: {
                show: false
            }
        }

        },
        clientTweetSeries: [{
          name: "Количество",
          data: [1216, 792, 741, 248, 133, 120]
        }],
        hashtagsTweetOptions: {
          noData: {
              text: 'Не найдено...'
          },
          chart: {
        id:"chartLang",
        type: 'bar',
    },
    plotOptions: {
        bar: {
            horizontal: true,
        }
    },

    dataLabels: {
        enabled: true,
        textAnchor: 'start',
        style: {
            colors: ['#fff']
        },
        formatter: function (val, opt) {
            return opt.w.globals.labels[opt.dataPointIndex] + ":  " + val
        },
        offsetX: 0,
        dropShadow: {
            enabled: true,
            top: 0,
            left: 0,
            blur: 1,
            opacity: 4.5
        }
        },
        yaxis: {
            labels: {
                show: false
            }
        },
        xaxis: {
            categories: ['SOULSaturday', 'TeamJoe', 'LGBTQ', 'WorldPressFreedomDay', 'TodosConBiden', 'VEDay', 'EqualityAct', 'League46', 'AB5', 'GunViolenceAwarenessDay', 'WorkersFirst', 'Juneteenth', 'DCStatehood', 'PrideMonth', 'ImmigrantHeritageMonth', 'NoBanAct', 'OpeningDay', 'CelebrationForChange', 'EidAlAdha', 'DemConvention', 'WomensEqualityDay', 'NationalDogDay', 'FabFive', 'RoshHashanah', 'BidenTownHall', 'NationalBlackVoterDay', 'NationalVoterRegistrationDay', 'OctoberVoter', 'WorldTeachersDay', 'ImVotingFor', 'IASen', 'NationalDessertDay', 'SpiritDay', 'VoteEarlyDay', 'OnlyTheYoung', 'BidenForFL', 'RockinEve', 'Inauguration2021', 'LunarNewYear', 'InternationalWomensDay'],
            labels: {
                show: false
            }
        }

        },
        hashtagsTweetSeries: [{
          name: "Количество",
          data: [4, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 13, 1, 1, 1, 1, 6, 1, 2, 1, 1, 3, 1, 1, 1, 5, 1, 1, 1, 2, 1, 1]

        }],
        urlsTweetOptions: {
          noData: {
              text: 'Не найдено...'
          },
          chart: {
        id:"chartLang",
        type: 'bar',
        // height: 300
    },
    plotOptions: {
        bar: {
            horizontal: true,
        }
    },

    dataLabels: {
        enabled: true,
        textAnchor: 'start',
        style: {
            colors: ['#fff']
        },
        formatter: function (val, opt) {
            return opt.w.globals.labels[opt.dataPointIndex] + ":  " + val
        },
        offsetX: 0,
        dropShadow: {
            enabled: true,
            top: 0,
            left: 0,
            blur: 1,
            opacity: 4.5
        }
        },
        yaxis: {
            labels: {
                show: false
            }
        },
        xaxis: {
            categories: ['twitter.com', 'iwillvote.com;', 'www.pscp.tv', 'iwillvote.com', 'joe.link', 'IWillVote.com;', 'JoeBiden.com'],
            labels: {
                show: false
            }
        }

        },
        urlsTweetSeries: [{
          name: "Количество",
          data: [2003, 52, 38, 23, 12, 11, 6]
        }],
        quotesTweetOptions: {
          noData: {
              text: 'Не найдено...'
          },
          chart: {
        id:"chartLang",
        type: 'bar',
        height: 300
    },
    plotOptions: {
        bar: {
            horizontal: true,
        }
    },

    dataLabels: {
        enabled: true,
        textAnchor: 'start',
        style: {
            colors: ['#fff']
        },
        formatter: function (val, opt) {
            return opt.w.globals.labels[opt.dataPointIndex] + ":  " + val
        },
        offsetX: 0,
        dropShadow: {
            enabled: true,
            top: 0,
            left: 0,
            blur: 1,
            opacity: 4.5
        }
        },
        yaxis: {
            labels: {
                show: false
            }
        },
        xaxis: {
            categories: ['truth', 'stevenmnuchin1', 'staceyabrams', 'Lawrence', 'springsteen', 'JoeBiden', 'realDonaldTrump'],
            labels: {
                show: false
            }
        }

        },
        quotesTweetSeries: [{
          name: "Количество",
          data: [1, 1, 3, 1, 1, 1, 6]
        }],
        retweetsTweetOptions: {
          noData: {
              text: 'Не найдено...'
          },
          chart: {
        id:"chartLang",
        type: 'bar',
        height: 300
    },
    plotOptions: {
        bar: {
            horizontal: true,
        }
    },

    dataLabels: {
        enabled: true,
        textAnchor: 'start',
        style: {
            colors: ['#fff']
        },
        formatter: function (val, opt) {
            return opt.w.globals.labels[opt.dataPointIndex] + ":  " + val
        },
        offsetX: 0,
        dropShadow: {
            enabled: true,
            top: 0,
            left: 0,
            blur: 1,
            opacity: 4.5
        }
        },
        yaxis: {
            labels: {
                show: false
            }
        },
        xaxis: {
            categories: ['staceyabrams', 'springsteen', 'nowthisnews', 'johnlegend', 'ewarren', 'ericswalwell', 'cindymccain', 'WhiteHouse'],
            labels: {
                show: false
            }
        }

        },
        retweetsTweetSeries: [{
          name: "Количество",
          data: [1, 1, 1, 1, 1, 1, 1, 5]
        }],
        usersTweetOptions: {
          noData: {
              text: 'Не найдено...'
          },
          chart: {
        id:"chartLang",
        type: 'bar',
        height: 300
    },
    plotOptions: {
        bar: {
            horizontal: true,
        }
    },

    dataLabels: {
        enabled: true,
        textAnchor: 'start',
        style: {
            colors: ['#fff']
        },
        formatter: function (val, opt) {
            return opt.w.globals.labels[opt.dataPointIndex] + ":  " + val
        },
        offsetX: 0,
        dropShadow: {
            enabled: true,
            top: 0,
            left: 0,
            blur: 1,
            opacity: 4.5
        }
        },
        yaxis: {
            labels: {
                show: false
            }
        },
        xaxis: {
            categories: ['washingtonpost', 'voxdotcom', 'tparti'],
            labels: {
                show: false
            }
        }

        },
        usersTweetSeries: [{
          name: "Количество",
          data: [9, 2, 1]
        }],

    methods: {
      async download() {
        try {
          await axios.get(`http://127.0.0.1:8000/twitter/person/${this.username}/`, {
              headers: {
                'Authorization': 'Token ' + this.$store.state.token
              }
            }
        ).then(response => {
            console.log('200')
          })
        } catch (Error) {
          this.isFalseLogin = true
        }
     }
    }
    }
    }
  }
</script>

<style>
  .small {
    max-width: 90%;
    margin:  0 auto;
  }
  .card_info {
    padding: 10px;
  }
  #username {
    font-family: 'Courier New', Courier, monospace;
    font-size: 15px;
  }
  #screen_name, .stat_caption {
    color: grey;
    opacity: 95%;
    font-size: 15px;
  }
  .stat_number {
    font-family: 'Courier New', Courier, monospace;
    font-size: 15px;
  }
</style>