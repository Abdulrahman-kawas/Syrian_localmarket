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
  onCallSeller,
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
  container: {
    flex: 1,
    backgroundColor: theme.colors.light.bg,
  },
  imageContainer: {
    height: 300,
    backgroundColor: theme.colors.light.bgSunk,
  },
  imagePlaceholder: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  imagePlaceholderText: {
    fontSize: theme.typography.sizes.body,
    color: theme.colors.light.textSoft,
  },
  content: {
    padding: theme.spacing.screenPadding,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: theme.spacing.md,
  },
  title: {
    fontSize: theme.typography.sizes.screenHeadline,
    fontWeight: theme.typography.weights.extraBold,
    color: theme.colors.light.text,
    flex: 1,
  },
  nearExpiryBadge: {
    backgroundColor: theme.colors.coral,
    paddingHorizontal: theme.spacing.sm,
    paddingVertical: theme.spacing.xs,
    borderRadius: theme.borderRadius.chip,
    marginLeft: theme.spacing.sm,
  },
  nearExpiryText: {
    fontSize: theme.typography.sizes.micro,
    fontWeight: theme.typography.weights.extraBold,
    color: '#FFFFFF',
  },
  description: {
    fontSize: theme.typography.sizes.body,
    color: theme.colors.light.textSoft,
    marginBottom: theme.spacing.xl,
    lineHeight: 24,
  },
  priceContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: theme.spacing.xl,
  },
  discountedPrice: {
    fontSize: theme.typography.sizes.priceHero,
    fontWeight: theme.typography.weights.extraBold,
    color: theme.colors.brass,
    marginRight: theme.spacing.md,
  },
  originalPrice: {
    fontSize: theme.typography.sizes.priceCard,
    color: theme.colors.light.textSoft,
    textDecorationLine: 'line-through',
  },
  expiryCard: {
    marginBottom: theme.spacing.md,
  },
  expiryLabel: {
    fontSize: theme.typography.sizes.caption,
    color: theme.colors.light.textSoft,
    marginBottom: theme.spacing.xs,
  },
  expiryDate: {
    fontSize: theme.typography.sizes.body,
    fontWeight: theme.typography.weights.bold,
    color: theme.colors.light.text,
  },
  expiryClass: {
    fontSize: theme.typography.sizes.caption,
    color: theme.colors.light.textSoft,
    marginTop: theme.spacing.xs,
  },
  sellerCard: {
    marginBottom: theme.spacing.md,
  },
  sellerLabel: {
    fontSize: theme.typography.sizes.caption,
    color: theme.colors.light.textSoft,
    marginBottom: theme.spacing.xs,
  },
  sellerName: {
    fontSize: theme.typography.sizes.body,
    fontWeight: theme.typography.weights.bold,
    color: theme.colors.light.text,
    marginBottom: theme.spacing.xs,
  },
  sellerPhone: {
    fontSize: theme.typography.sizes.body,
    color: theme.colors.brass,
  },
  safetyCard: {
    backgroundColor: theme.colors.light.bgSunk,
    marginBottom: theme.spacing.xl,
  },
  safetyText: {
    fontSize: theme.typography.sizes.caption,
    color: theme.colors.light.textSoft,
    fontStyle: 'italic',
  },
  actions: {
    gap: theme.spacing.md,
  },
});

export default ListingDetail;
