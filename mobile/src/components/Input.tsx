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
  label: {
    fontSize: theme.typography.sizes.caption,
    fontWeight: theme.typography.weights.medium,
    color: theme.colors.light.text,
    marginBottom: theme.spacing.xs,
  },
  input: {
    height: 50,
    backgroundColor: theme.colors.light.bgSunk,
    borderRadius: theme.borderRadius.button,
    paddingHorizontal: theme.spacing.lg,
    fontSize: theme.typography.sizes.body,
    color: theme.colors.light.text,
    borderWidth: 1,
    borderColor: theme.colors.light.line,
  },
  inputError: {
    borderColor: theme.colors.coral,
  },
  error: {
    fontSize: theme.typography.sizes.micro,
    color: theme.colors.coral,
    marginTop: theme.spacing.xs,
  },
});

export default Input;
