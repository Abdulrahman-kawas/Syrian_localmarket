import React from 'react';
import { TextInput, View, Text, StyleSheet, TextInputProps } from 'react-native';
import { theme } from '../theme';

interface InputProps extends TextInputProps {
  label?: string;
  error?: string;
}

const Input: React.FC<InputProps> = ({ label, error, ...props }) => {
  return (
    <View style={styles.container}>
      {label && <Text style={styles.label}>{label}</Text>}
      <TextInput
        style={[styles.input, error ? styles.inputError : null]}
        placeholderTextColor={theme.colors.light.textSoft}
        {...props}
      />
      {error && <Text style={styles.error}>{error}</Text>}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    marginBottom: theme.spacing.lg,
  },
  error: {
    color: theme.colors.coral,
    fontSize: theme.typography.sizes.micro,
    marginTop: theme.spacing.xs,
  },
  input: {
    backgroundColor: theme.colors.light.bgSunk,
    borderColor: theme.colors.light.line,
    borderRadius: theme.borderRadius.button,
    borderWidth: 1,
    color: theme.colors.light.text,
    fontSize: theme.typography.sizes.body,
    height: 50,
    paddingHorizontal: theme.spacing.lg,
  },
  inputError: {
    borderColor: theme.colors.coral,
  },
  label: {
    color: theme.colors.light.text,
    fontSize: theme.typography.sizes.caption,
    fontWeight: theme.typography.weights.medium,
    marginBottom: theme.spacing.xs,
  },
});

export default Input;
