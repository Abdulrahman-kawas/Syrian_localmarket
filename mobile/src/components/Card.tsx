import React from 'react';
import { View, StyleSheet, ViewStyle } from 'react-native';
import { theme } from '../theme';

interface CardProps {
  children: React.ReactNode;
  style?: ViewStyle;
}

const Card: React.FC<CardProps> = ({ children, style }) => {
  return <View style={[styles.card, style]}>{children}</View>;
};

const styles = StyleSheet.create({
  card: {
    backgroundColor: theme.colors.light.bgElev,
    borderRadius: theme.borderRadius.card,
    borderWidth: 1,
    borderColor: theme.colors.light.line,
    padding: theme.spacing.lg,
    ...theme.shadows.lightCard,
  },
});

export default Card;
