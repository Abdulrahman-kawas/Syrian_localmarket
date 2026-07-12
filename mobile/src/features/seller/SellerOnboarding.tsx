import React, { useState } from 'react';
import { View, Text, StyleSheet, ScrollView } from 'react-native';
import { Button, Input } from '../../components';
import { theme } from '../../theme';

interface SellerOnboardingProps {
  onComplete: (data: {
    type: 'shop' | 'factory';
    shopName: string;
    categoryId: string;
    location: {
      latitude: number;
      longitude: number;
      plusCode: string;
      description: string;
    };
  }) => void;
}

const SellerOnboarding: React.FC<SellerOnboardingProps> = ({ onComplete }) => {
  const [type, setType] = useState<'shop' | 'factory'>('shop');
  const [shopName, setShopName] = useState('');
  const [location, setLocation] = useState({
    latitude: 0,
    longitude: 0,
    plusCode: '',
    description: '',
  });

  const handleComplete = () => {
    onComplete({
      type,
      shopName,
      categoryId: '', // Will be selected from categories
      location,
    });
  };

  return (
    <ScrollView style={styles.container}>
      <Text style={styles.title}>Seller Onboarding</Text>
      <Text style={styles.subtitle}>Set up your shop or factory profile</Text>

      <View style={styles.typeSelector}>
        <Button
          title="Shop"
          variant={type === 'shop' ? 'primary' : 'ghost'}
          onPress={() => setType('shop')}
        />
        <Button
          title="Factory"
          variant={type === 'factory' ? 'primary' : 'ghost'}
          onPress={() => setType('factory')}
        />
      </View>

      <Input
        label="Shop Name"
        value={shopName}
        onChangeText={setShopName}
        placeholder="Enter shop name"
      />

      <Input
        label="Location Description"
        value={location.description}
        onChangeText={(text) => setLocation({ ...location, description: text })}
        placeholder="e.g., Near Umayyad Mosque"
      />

      <Button title="Complete Setup" onPress={handleComplete} />
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    backgroundColor: theme.colors.light.bg,
    flex: 1,
    padding: theme.spacing.screenPadding,
  },
  subtitle: {
    color: theme.colors.light.textSoft,
    fontSize: theme.typography.sizes.body,
    marginBottom: theme.spacing.xl,
  },
  title: {
    color: theme.colors.light.text,
    fontSize: theme.typography.sizes.screenHeadline,
    fontWeight: theme.typography.weights.extraBold,
    marginBottom: theme.spacing.sm,
  },
  typeSelector: {
    flexDirection: 'row',
    gap: theme.spacing.md,
    marginBottom: theme.spacing.xl,
  },
});

export default SellerOnboarding;
