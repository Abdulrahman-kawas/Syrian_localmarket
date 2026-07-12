import React from 'react';
import { View, Text, StyleSheet, FlatList, TouchableOpacity } from 'react-native';
import { Card } from '../../components';
import { theme } from '../../theme';

interface Product {
  id: string;
  title: string;
  type: 'regular' | 'market_discount' | 'near_expiry';
  originalPrice: number;
  discountedPrice: number;
  expiryDate?: string;
  quantity: number;
  seller: {
    id: string;
    shopName: string;
  };
}

interface ListingFeedProps {
  products: Product[];
  onProductPress: (product: Product) => void;
}

const ListingFeed: React.FC<ListingFeedProps> = ({ products, onProductPress }) => {
  const renderProduct = ({ item }: { item: Product }) => (
    <TouchableOpacity onPress={() => onProductPress(item)}>
      <Card style={styles.card}>
        <View style={styles.header}>
          <Text style={styles.title} numberOfLines={1}>
            {item.title}
          </Text>
          {item.type === 'near_expiry' && (
            <View style={styles.nearExpiryBadge}>
              <Text style={styles.nearExpiryText}>Near Expiry</Text>
            </View>
          )}
        </View>

        <Text style={styles.seller}>{item.seller.shopName}</Text>

        <View style={styles.priceContainer}>
          <Text style={styles.discountedPrice}>{item.discountedPrice} SYP</Text>
          <Text style={styles.originalPrice}>{item.originalPrice} SYP</Text>
        </View>

        {item.expiryDate && (
          <Text style={styles.expiry}>Expires: {item.expiryDate}</Text>
        )}

        <Text style={styles.quantity}>Qty: {item.quantity}</Text>
      </Card>
    </TouchableOpacity>
  );

  return (
    <FlatList
      data={products}
      renderItem={renderProduct}
      keyExtractor={(item) => item.id}
      contentContainerStyle={styles.list}
    />
  );
};

const styles = StyleSheet.create({
  card: {
    marginBottom: theme.spacing.md,
  },
  discountedPrice: {
    color: theme.colors.brass,
    fontSize: theme.typography.sizes.priceCard,
    fontWeight: theme.typography.weights.extraBold,
    marginRight: theme.spacing.sm,
  },
  expiry: {
    color: theme.colors.light.textSoft,
    fontSize: theme.typography.sizes.caption,
    marginBottom: theme.spacing.xs,
  },
  header: {
    alignItems: 'center',
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: theme.spacing.sm,
  },
  list: {
    padding: theme.spacing.screenPadding,
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
    fontSize: theme.typography.sizes.priceWas,
    textDecorationLine: 'line-through',
  },
  priceContainer: {
    alignItems: 'center',
    flexDirection: 'row',
    marginBottom: theme.spacing.sm,
  },
  quantity: {
    color: theme.colors.light.textSoft,
    fontSize: theme.typography.sizes.caption,
  },
  seller: {
    color: theme.colors.light.textSoft,
    fontSize: theme.typography.sizes.caption,
    marginBottom: theme.spacing.sm,
  },
  title: {
    color: theme.colors.light.text,
    flex: 1,
    fontSize: theme.typography.sizes.cardTitle,
    fontWeight: theme.typography.weights.bold,
  },
});

export default ListingFeed;
