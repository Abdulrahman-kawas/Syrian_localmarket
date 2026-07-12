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
  qrCodeUrl,
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
    flex: 1,
    backgroundColor: theme.colors.light.bg,
    padding: theme.spacing.screenPadding,
    alignItems: 'center',
  },
  title: {
    fontSize: theme.typography.sizes.sectionTitle,
    fontWeight: theme.typography.weights.extraBold,
    color: theme.colors.light.text,
    marginBottom: theme.spacing.xl,
  },
  qrContainer: {
    marginBottom: theme.spacing.xl,
  },
  qrFrame: {
    width: 196,
    height: 196,
    backgroundColor: '#FFFFFF',
    borderRadius: theme.borderRadius.qrCard,
    justifyContent: 'center',
    alignItems: 'center',
    ...theme.shadows.lightCard,
  },
  qrPlaceholder: {
    width: 150,
    height: 150,
    backgroundColor: theme.colors.light.bgSunk,
    borderRadius: 8,
    justifyContent: 'center',
    alignItems: 'center',
  },
  qrText: {
    fontSize: theme.typography.sizes.sectionTitle,
    fontWeight: theme.typography.weights.extraBold,
    color: theme.colors.pine,
  },
  productInfo: {
    alignItems: 'center',
    marginBottom: theme.spacing.xl,
  },
  productTitle: {
    fontSize: theme.typography.sizes.cardTitle,
    fontWeight: theme.typography.weights.bold,
    color: theme.colors.light.text,
    marginBottom: theme.spacing.xs,
  },
  productPrice: {
    fontSize: theme.typography.sizes.priceHero,
    fontWeight: theme.typography.weights.extraBold,
    color: theme.colors.brass,
  },
  note: {
    fontSize: theme.typography.sizes.caption,
    color: theme.colors.light.textSoft,
    textAlign: 'center',
    marginBottom: theme.spacing.xl,
  },
});

export default QRDisplay;
