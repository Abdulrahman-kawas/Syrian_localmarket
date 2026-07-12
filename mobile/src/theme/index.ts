export const theme = {
  colors: {
    // Brand constants
    pine: '#0F3D2E',
    pine600: '#155540',
    brass: '#C9A24B',
    brassSoft: '#D8B876',
    coral: '#E8763A',
    ivory: '#F6F2E9',
    ink: '#0A1F17',

    // Light theme
    light: {
      bg: '#F6F2E9',
      bgElev: '#FFFFFF',
      bgSunk: '#EEE8DA',
      text: '#132C22',
      textSoft: '#5C6B63',
      line: 'rgba(15,61,46,0.12)',
      primary: '#0F3D2E',
      onPrimary: '#F6F2E9',
      accent: '#C9A24B',
    },

    // Dark theme
    dark: {
      bg: '#0A1F17',
      bgElev: '#122A20',
      bgSunk: '#0E241B',
      text: '#EDE7D6',
      textSoft: '#9DB0A5',
      line: 'rgba(214,203,168,0.14)',
      primary: '#C9A24B',
      onPrimary: '#0A1F17',
      accent: '#D8B876',
    },

    // Status
    urgent: '#E8763A',
    mapBg: '#E7E2D3',
    mapRoad: '#D8D2C0',
    mapPark: '#DDE6CE',
    mapWater: '#CFE0DB',
  },

  spacing: {
    xs: 4,
    sm: 8,
    md: 12,
    md2: 14,
    lg: 16,
    lg2: 18,
    xl: 24,
    screenPadding: 18,
  },

  borderRadius: {
    button: 16,
    card: 20,
    heroCard: 24,
    qrCard: 26,
    thumbnail: 15,
    chip: 999,
    fab: 18,
  },

  typography: {
    // Arabic + display + body
    arabic: 'Tajawal',
    // Latin/English
    english: 'Plus Jakarta Sans',

    sizes: {
      screenHeadline: 26,
      sectionTitle: 17,
      cardTitle: 16,
      body: 15,
      priceHero: 24,
      priceCard: 17,
      priceWas: 14,
      caption: 12,
      micro: 10,
    },

    // `as const` keeps these as React Native fontWeight literals (e.g. '700')
    // rather than widening to `string`, which RN's TextStyle rejects.
    weights: {
      regular: '400',
      medium: '500',
      bold: '700',
      extraBold: '800',
    } as const,
  },

  shadows: {
    lightCard: {
      shadowColor: '#0F3D2E',
      shadowOffset: { width: 0, height: 12 },
      shadowOpacity: 0.35,
      shadowRadius: 30,
      elevation: 8,
    },
    darkCard: {
      shadowColor: '#000000',
      shadowOffset: { width: 0, height: 18 },
      shadowOpacity: 0.7,
      shadowRadius: 40,
      elevation: 12,
    },
    primaryButton: {
      shadowColor: '#0F3D2E',
      shadowOffset: { width: 0, height: 14 },
      shadowOpacity: 0.7,
      shadowRadius: 30,
      elevation: 10,
    },
  },
};

export type Theme = typeof theme;
