 <template>
    <v-footer
      dark
      padless
      class="mt-4"
    >
      <v-card
        flat
        tile
        class="lighten-1 white--text text-center"
      >
        <v-card-text>
          <v-btn
            v-for="icon in icons"
            :key="icon"
            class="mx-4 white--text"
            icon
          >
            <v-icon size="24px">
              {{ icon }}
            </v-icon>
          </v-btn>
        </v-card-text>
  
        <v-card-text class="white--text pt-0">
          Непрерывно в глобальной сети Интернет публикуется негативный
            контент, повсеместное распространение которого ведет к дестабилизации общественнополитической ситуации в Российской Федерации, популяризации материалов
            террористических и экстремистских организаций, призывам к массовым беспорядкам,
            осуществлению экстремистской деятельности, участию в массовых (публичных)
            мероприятиях, проводимых с нарушением установленного порядка, совершению
            самоубийства, осуществлению пропаганды криминального образа жизни, потреблению
            наркотических средств и психотропных веществ, размещению иной противоправной
            информации. Основным объектом такого деструктивного воздействия является молодежь.
        </v-card-text>
  
        <v-divider></v-divider>
  
        <v-card-text class="white--text">
          {{ new Date().getFullYear() }} — <strong>OSIRIS</strong>
        </v-card-text>
      </v-card>
    </v-footer>
</template>

<script>
  export default {
    name: 'Footer',
    data: () => ({
    icons: [
      'mdi-facebook',
      'mdi-twitter',
      'mdi-linkedin',
      'mdi-instagram',
    ],
  }),
  }
</script>