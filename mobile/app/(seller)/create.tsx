import { View, StyleSheet, Alert } from 'react-native';
import { useRouter } from 'expo-router';
import { ListingCreate } from '../../src/features/seller';
import { createProduct } from '../../src/api/endpoints';
import { theme } from '../../src/theme';
import i18n from '../../src/i18n';

export default function CreateListing() {
  const router = useRouter();

  async function onSubmit(data: {
    title: string;
    description: string;
    type: 'regular' | 'market_discount' | 'near_expiry';
    originalPrice: number;
    discountedPrice: number;
    expiryDate?: string;
    expiryClass?: 'best_before' | 'use_by';
    quantity: number;
  }) {
    try {
      await createProduct(data);
      Alert.alert(i18n.t('success'), '', [
        { text: 'OK', onPress: () => router.replace('/(seller)/listings') },
      ]);
    } catch (e) {
      Alert.alert(i18n.t('error'), e instanceof Error ? e.message : 'Error');
    }
  }

  return (
    <View style={styles.container}>
      <ListingCreate onSubmit={onSubmit} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: theme.colors.light.bg },
});
