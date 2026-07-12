import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { Button } from '../../components';
import { theme } from '../../theme';

interface QRDisplayProps {
  productTitle: string;
  productPrice: number;
  qrCodeUrl: string;
  onPrint: () => void;
}

const QRDisplay: React.FC<QRDisplayProps> = ({
  productTitle,
  productPrice,
  onPrint,
}) => {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Product QR Code</Text>

      <View style={styles.qrContainer}>
        <View style={styles.qrFrame}>
          {/* QR code image would be rendered here */}
          <View style={styles.qrPlaceholder}>
            <Text style={styles.qrText}>QR</Text>
          </View>
        </View>
      </View>

      <View style={styles.productInfo}>
        <Text style={styles.productTitle}>{productTitle}</Text>
        <Text style={styles.productPrice}>{productPrice} SYP</Text>
      </View>

      <Text style={styles.note}>
        Display this QR code in your shop. Customers can scan it to purchase.
      </Text>

      <Button title="Print QR Code" onPress={onPrint} variant="ghost" />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    alignItems: 'center',
    backgroundColor: theme.colors.light.bg,
    flex: 1,
    padding: theme.spacing.screenPadding,
  },
  note: {
    color: theme.colors.light.textSoft,
    fontSize: theme.typography.sizes.caption,
    marginBottom: theme.spacing.xl,
    textAlign: 'center',
  },
  productInfo: {
    alignItems: 'center',
    marginBottom: theme.spacing.xl,
  },
  productPrice: {
    color: theme.colors.brass,
    fontSize: theme.typography.sizes.priceHero,
    fontWeight: theme.typography.weights.extraBold,
  },
  productTitle: {
    color: theme.colors.light.text,
    fontSize: theme.typography.sizes.cardTitle,
    fontWeight: theme.typography.weights.bold,
    marginBottom: theme.spacing.xs,
  },
  qrContainer: {
    marginBottom: theme.spacing.xl,
  },
  qrFrame: {
    alignItems: 'center',
    backgroundColor: theme.colors.white,
    borderRadius: theme.borderRadius.qrCard,
    height: 196,
    justifyContent: 'center',
    width: 196,
    ...theme.shadows.lightCard,
  },
  qrPlaceholder: {
    alignItems: 'center',
    backgroundColor: theme.colors.light.bgSunk,
    borderRadius: 8,
    height: 150,
    justifyContent: 'center',
    width: 150,
  },
  qrText: {
    color: theme.colors.pine,
    fontSize: theme.typography.sizes.sectionTitle,
    fontWeight: theme.typography.weights.extraBold,
  },
  title: {
    color: theme.colors.light.text,
    fontSize: theme.typography.sizes.sectionTitle,
    fontWeight: theme.typography.weights.extraBold,
    marginBottom: theme.spacing.xl,
  },
});

export default QRDisplay;
