import React from 'react';
import { View, Text, StyleSheet, ScrollView, Linking } from 'react-native';
import { Button, Card } from '../../components';
import { theme } from '../../theme';

interface Product {
  id: string;
  title: string;
  description: string;
  type: 'regular' | 'market_discount' | 'near_expiry';
  originalPrice: number;
  discountedPrice: number;
  expiryDate?: string;
  expiryClass?: 'best_before' | 'use_by';
  quantity: number;
  images: string[];
  seller: {
    id: string;
    shopName: string;
    phone: string;
  };
}

interface ListingDetailProps {
  product: Product;
  onCallSeller: () => void;
  onChatSeller: () => void;
  onScanQR: () => void;
}

const ListingDetail: React.FC<ListingDetailProps> = ({
  product,
  onChatSeller,
  onScanQR,
}) => {
  const handleCall = () => {
    Linking.openURL(`tel:${product.seller.phone}`);
  };

  return (
    <ScrollView style={styles.container}>
      <View style={styles.imageContainer}>
        {/* Product images would be rendered here */}
        <View style={styles.imagePlaceholder}>
          <Text style={styles.imagePlaceholderText}>Product Image</Text>
        </View>
      </View>

      <View style={styles.content}>
        <View style={styles.header}>
          <Text style={styles.title}>{product.title}</Text>
          {product.type === 'near_expiry' && (
            <View style={styles.nearExpiryBadge}>
              <Text style={styles.nearExpiryText}>Near Expiry</Text>
            </View>
          )}
        </View>

        <Text style={styles.description}>{product.description}</Text>

        <View style={styles.priceContainer}>
          <Text style={styles.discountedPrice}>{product.discountedPrice} SYP</Text>
          <Text style={styles.originalPrice}>{product.originalPrice} SYP</Text>
        </View>

        {product.expiryDate && (
          <Card style={styles.expiryCard}>
            <Text style={styles.expiryLabel}>Expires:</Text>
            <Text style={styles.expiryDate}>{product.expiryDate}</Text>
            {product.expiryClass && (
              <Text style={styles.expiryClass}>
                ({product.expiryClass === 'best_before' ? 'Best Before' : 'Use By'})
              </Text>
            )}
          </Card>
        )}

        <Card style={styles.sellerCard}>
          <Text style={styles.sellerLabel}>Seller:</Text>
          <Text style={styles.sellerName}>{product.seller.shopName}</Text>
          <Text style={styles.sellerPhone}>{product.seller.phone}</Text>
        </Card>

        <Card style={styles.safetyCard}>
          <Text style={styles.safetyText}>
            Please inspect the product on pickup. The platform only connects sellers and buyers.
          </Text>
        </Card>

        <View style={styles.actions}>
          <Button title="Call Seller" onPress={handleCall} variant="ghost" />
          <Button title="Chat" onPress={onChatSeller} variant="ghost" />
          <Button title="Scan QR" onPress={onScanQR} />
        </View>
      </View>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  actions: {
    gap: theme.spacing.md,
  },
  container: {
    backgroundColor: theme.colors.light.bg,
    flex: 1,
  },
  content: {
    padding: theme.spacing.screenPadding,
  },
  description: {
    color: theme.colors.light.textSoft,
    fontSize: theme.typography.sizes.body,
    lineHeight: 24,
    marginBottom: theme.spacing.xl,
  },
  discountedPrice: {
    color: theme.colors.brass,
    fontSize: theme.typography.sizes.priceHero,
    fontWeight: theme.typography.weights.extraBold,
    marginRight: theme.spacing.md,
  },
  expiryCard: {
    marginBottom: theme.spacing.md,
  },
  expiryClass: {
    color: theme.colors.light.textSoft,
    fontSize: theme.typography.sizes.caption,
    marginTop: theme.spacing.xs,
  },
  expiryDate: {
    color: theme.colors.light.text,
    fontSize: theme.typography.sizes.body,
    fontWeight: theme.typography.weights.bold,
  },
  expiryLabel: {
    color: theme.colors.light.textSoft,
    fontSize: theme.typography.sizes.caption,
    marginBottom: theme.spacing.xs,
  },
  header: {
    alignItems: 'center',
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: theme.spacing.md,
  },
  imageContainer: {
    backgroundColor: theme.colors.light.bgSunk,
    height: 300,
  },
  imagePlaceholder: {
    alignItems: 'center',
    flex: 1,
    justifyContent: 'center',
  },
  imagePlaceholderText: {
    color: theme.colors.light.textSoft,
    fontSize: theme.typography.sizes.body,
  },
  nearExpiryBadge: {
    backgroundColor: theme.colors.coral,
    borderRadius: theme.borderRadius.chip,
    marginLeft: theme.spacing.sm,
    paddingHorizontal: theme.spacing.sm,
    paddingVertical: theme.spacing.xs,
  },
  nearExpiryText: {
    color: theme.colors.white,
    fontSize: theme.typography.sizes.micro,
    fontWeight: theme.typography.weights.extraBold,
  },
  originalPrice: {
    color: theme.colors.light.textSoft,
    fontSize: theme.typography.sizes.priceCard,
    textDecorationLine: 'line-through',
  },
  priceContainer: {
    alignItems: 'center',
    flexDirection: 'row',
    marginBottom: theme.spacing.xl,
  },
  safetyCard: {
    backgroundColor: theme.colors.light.bgSunk,
    marginBottom: theme.spacing.xl,
  },
  safetyText: {
    color: theme.colors.light.textSoft,
    fontSize: theme.typography.sizes.caption,
    fontStyle: 'italic',
  },
  sellerCard: {
    marginBottom: theme.spacing.md,
  },
  sellerLabel: {
    color: theme.colors.light.textSoft,
    fontSize: theme.typography.sizes.caption,
    marginBottom: theme.spacing.xs,
  },
  sellerName: {
    color: theme.colors.light.text,
    fontSize: theme.typography.sizes.body,
    fontWeight: theme.typography.weights.bold,
    marginBottom: theme.spacing.xs,
  },
  sellerPhone: {
    color: theme.colors.brass,
    fontSize: theme.typography.sizes.body,
  },
  title: {
    color: theme.colors.light.text,
    flex: 1,
    fontSize: theme.typography.sizes.screenHeadline,
    fontWeight: theme.typography.weights.extraBold,
  },
});

export default ListingDetail;
