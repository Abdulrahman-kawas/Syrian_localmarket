import React, { useState } from 'react';
import { View, Text, StyleSheet, ScrollView } from 'react-native';
import { Button, Input } from '../../components';
import { theme } from '../../theme';

interface ListingEditProps {
  listing: {
    id: string;
    title: string;
    description: string;
    type: 'regular' | 'market_discount' | 'near_expiry';
    originalPrice: number;
    discountedPrice: number;
    expiryDate?: string;
    expiryClass?: 'best_before' | 'use_by';
    quantity: number;
  };
  onSubmit: (data: {
    title: string;
    description: string;
    type: 'regular' | 'market_discount' | 'near_expiry';
    originalPrice: number;
    discountedPrice: number;
    expiryDate?: string;
    expiryClass?: 'best_before' | 'use_by';
    quantity: number;
  }) => void;
}

const ListingEdit: React.FC<ListingEditProps> = ({ listing, onSubmit }) => {
  const [title, setTitle] = useState(listing.title);
  const [description, setDescription] = useState(listing.description);
  const [type, setType] = useState(listing.type);
  const [originalPrice, setOriginalPrice] = useState(listing.originalPrice.toString());
  const [discountedPrice, setDiscountedPrice] = useState(listing.discountedPrice.toString());
  const [expiryDate, setExpiryDate] = useState(listing.expiryDate || '');
  const [expiryClass, setExpiryClass] = useState(listing.expiryClass || 'best_before');
  const [quantity, setQuantity] = useState(listing.quantity.toString());

  const handleSubmit = () => {
    onSubmit({
      title,
      description,
      type,
      originalPrice: parseFloat(originalPrice),
      discountedPrice: parseFloat(discountedPrice),
      expiryDate: expiryDate || undefined,
      expiryClass: type === 'near_expiry' ? expiryClass : undefined,
      quantity: parseInt(quantity, 10),
    });
  };

  return (
    <ScrollView style={styles.container}>
      <Text style={styles.title}>Edit Listing</Text>

      <Input
        label="Title"
        value={title}
        onChangeText={setTitle}
        placeholder="Product title"
      />

      <Input
        label="Description"
        value={description}
        onChangeText={setDescription}
        placeholder="Product description"
        multiline
      />

      <View style={styles.typeSelector}>
        <Button
          title="Regular"
          variant={type === 'regular' ? 'primary' : 'ghost'}
          onPress={() => setType('regular')}
        />
        <Button
          title="Market Discount"
          variant={type === 'market_discount' ? 'primary' : 'ghost'}
          onPress={() => setType('market_discount')}
        />
        <Button
          title="Near Expiry"
          variant={type === 'near_expiry' ? 'primary' : 'ghost'}
          onPress={() => setType('near_expiry')}
        />
      </View>

      <Input
        label="Original Price"
        value={originalPrice}
        onChangeText={setOriginalPrice}
        placeholder="0.00"
        keyboardType="numeric"
      />

      <Input
        label="Discounted Price"
        value={discountedPrice}
        onChangeText={setDiscountedPrice}
        placeholder="0.00"
        keyboardType="numeric"
      />

      {type === 'near_expiry' && (
        <>
          <Input
            label="Expiry Date"
            value={expiryDate}
            onChangeText={setExpiryDate}
            placeholder="YYYY-MM-DD"
          />

          <View style={styles.expiryClassSelector}>
            <Button
              title="Best Before"
              variant={expiryClass === 'best_before' ? 'primary' : 'ghost'}
              onPress={() => setExpiryClass('best_before')}
            />
            <Button
              title="Use By"
              variant={expiryClass === 'use_by' ? 'primary' : 'ghost'}
              onPress={() => setExpiryClass('use_by')}
            />
          </View>
        </>
      )}

      <Input
        label="Quantity"
        value={quantity}
        onChangeText={setQuantity}
        placeholder="0"
        keyboardType="numeric"
      />

      <Button title="Save Changes" onPress={handleSubmit} />
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    backgroundColor: theme.colors.light.bg,
    flex: 1,
    padding: theme.spacing.screenPadding,
  },
  expiryClassSelector: {
    flexDirection: 'row',
    gap: theme.spacing.sm,
    marginBottom: theme.spacing.xl,
  },
  title: {
    color: theme.colors.light.text,
    fontSize: theme.typography.sizes.screenHeadline,
    fontWeight: theme.typography.weights.extraBold,
    marginBottom: theme.spacing.xl,
  },
  typeSelector: {
    flexDirection: 'row',
    gap: theme.spacing.sm,
    marginBottom: theme.spacing.xl,
  },
});

export default ListingEdit;
