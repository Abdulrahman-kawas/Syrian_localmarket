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
  list: {
    padding: theme.spacing.screenPadding,
  },
  card: {
    marginBottom: theme.spacing.md,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: theme.spacing.sm,
  },
  title: {
    fontSize: theme.typography.sizes.cardTitle,
    fontWeight: theme.typography.weights.bold,
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
  seller: {
    fontSize: theme.typography.sizes.caption,
    color: theme.colors.light.textSoft,
    marginBottom: theme.spacing.sm,
  },
  priceContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: theme.spacing.sm,
  },
  discountedPrice: {
    fontSize: theme.typography.sizes.priceCard,
    fontWeight: theme.typography.weights.extraBold,
    color: theme.colors.brass,
    marginRight: theme.spacing.sm,
  },
  originalPrice: {
    fontSize: theme.typography.sizes.priceWas,
    color: theme.colors.light.textSoft,
    textDecorationLine: 'line-through',
  },
  expiry: {
    fontSize: theme.typography.sizes.caption,
    color: theme.colors.light.textSoft,
    marginBottom: theme.spacing.xs,
  },
  quantity: {
    fontSize: theme.typography.sizes.caption,
    color: theme.colors.light.textSoft,
  },
});

export default ListingFeed;
