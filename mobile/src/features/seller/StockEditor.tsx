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
  container: {
    backgroundColor: theme.colors.light.bgElev,
    borderRadius: theme.borderRadius.card,
    padding: theme.spacing.lg,
    borderWidth: 1,
    borderColor: theme.colors.light.line,
  },
  title: {
    fontSize: theme.typography.sizes.sectionTitle,
    fontWeight: theme.typography.weights.extraBold,
    color: theme.colors.light.text,
    marginBottom: theme.spacing.lg,
  },
  currentStock: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: theme.spacing.xl,
  },
  label: {
    fontSize: theme.typography.sizes.body,
    color: theme.colors.light.textSoft,
  },
  quantity: {
    fontSize: theme.typography.sizes.priceHero,
    fontWeight: theme.typography.weights.extraBold,
    color: theme.colors.brass,
  },
  actions: {
    flexDirection: 'row',
    gap: theme.spacing.md,
  },
  soldOut: {
    fontSize: theme.typography.sizes.cardTitle,
    fontWeight: theme.typography.weights.extraBold,
    color: theme.colors.coral,
    textAlign: 'center',
    marginTop: theme.spacing.lg,
  },
});

export default StockEditor;
