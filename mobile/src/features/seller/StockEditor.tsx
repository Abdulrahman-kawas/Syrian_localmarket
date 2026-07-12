import React, { useState } from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { Button, Input } from '../../components';
import { theme } from '../../theme';

interface StockEditorProps {
  currentQuantity: number;
  onUpdate: (quantity: number) => void;
}

const StockEditor: React.FC<StockEditorProps> = ({ currentQuantity, onUpdate }) => {
  const [quantity, setQuantity] = useState(currentQuantity.toString());

  const handleUpdate = () => {
    const newQuantity = parseInt(quantity, 10);
    if (!isNaN(newQuantity) && newQuantity >= 0) {
      onUpdate(newQuantity);
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Stock Editor</Text>

      <View style={styles.currentStock}>
        <Text style={styles.label}>Current Quantity:</Text>
        <Text style={styles.quantity}>{currentQuantity}</Text>
      </View>

      <Input
        label="New Quantity"
        value={quantity}
        onChangeText={setQuantity}
        placeholder="0"
        keyboardType="numeric"
      />

      <View style={styles.actions}>
        <Button
          title="Set to 0"
          variant="ghost"
          onPress={() => setQuantity('0')}
        />
        <Button
          title="Update Stock"
          onPress={handleUpdate}
        />
      </View>

      {currentQuantity === 0 && (
        <Text style={styles.soldOut}>Sold Out</Text>
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  actions: {
    flexDirection: 'row',
    gap: theme.spacing.md,
  },
  container: {
    backgroundColor: theme.colors.light.bgElev,
    borderColor: theme.colors.light.line,
    borderRadius: theme.borderRadius.card,
    borderWidth: 1,
    padding: theme.spacing.lg,
  },
  currentStock: {
    alignItems: 'center',
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: theme.spacing.xl,
  },
  label: {
    color: theme.colors.light.textSoft,
    fontSize: theme.typography.sizes.body,
  },
  quantity: {
    color: theme.colors.brass,
    fontSize: theme.typography.sizes.priceHero,
    fontWeight: theme.typography.weights.extraBold,
  },
  soldOut: {
    color: theme.colors.coral,
    fontSize: theme.typography.sizes.cardTitle,
    fontWeight: theme.typography.weights.extraBold,
    marginTop: theme.spacing.lg,
    textAlign: 'center',
  },
  title: {
    color: theme.colors.light.text,
    fontSize: theme.typography.sizes.sectionTitle,
    fontWeight: theme.typography.weights.extraBold,
    marginBottom: theme.spacing.lg,
  },
});

export default StockEditor;
