import React, { useState } from 'react';
import { View, Text, StyleSheet, ScrollView } from 'react-native';
import { Button, Input } from '../../components';
import { theme } from '../../theme';

interface ListingCreateProps {
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

const ListingCreate: React.FC<ListingCreateProps> = ({ onSubmit }) => {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [type, setType] = useState<'regular' | 'market_discount' | 'near_expiry'>('regular');
  const [originalPrice, setOriginalPrice] = useState('');
  const [discountedPrice, setDiscountedPrice] = useState('');
  const [expiryDate, setExpiryDate] = useState('');
  const [expiryClass, setExpiryClass] = useState<'best_before' | 'use_by'>('best_before');
  const [quantity, setQuantity] = useState('');

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
      <Text style={styles.title}>Create Listing</Text>

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

      <Button title="Create Listing" onPress={handleSubmit} />
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: theme.colors.light.bg,
    padding: theme.spacing.screenPadding,
  },
  title: {
    fontSize: theme.typography.sizes.screenHeadline,
    fontWeight: theme.typography.weights.extraBold,
    color: theme.colors.light.text,
    marginBottom: theme.spacing.xl,
  },
  typeSelector: {
    flexDirection: 'row',
    gap: theme.spacing.sm,
    marginBottom: theme.spacing.xl,
  },
  expiryClassSelector: {
    flexDirection: 'row',
    gap: theme.spacing.sm,
    marginBottom: theme.spacing.xl,
  },
});

export default ListingCreate;
