import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { Button } from '../../components';
import { theme } from '../../theme';

interface QRScannerProps {
  onScan: (code: string) => void;
  onCancel: () => void;
}

const QRScanner: React.FC<QRScannerProps> = ({ onScan: _onScan, onCancel }) => {
  return (
    <View style={styles.container}>
      <View style={styles.scannerContainer}>
        {/* Camera/QR scanner would be rendered here */}
        <View style={styles.scannerPlaceholder}>
          <Text style={styles.scannerPlaceholderText}>QR Scanner</Text>
        </View>
      </View>

      <View style={styles.infoContainer}>
        <Text style={styles.infoText}>
          Scan the seller&apos;s QR code to purchase this product.
        </Text>
        <Text style={styles.noteText}>
          No in-app payment. Only the seller confirms — no confirmation, no proof.
        </Text>
      </View>

      <View style={styles.actions}>
        <Button title="Cancel" onPress={onCancel} variant="ghost" />
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  actions: {
    backgroundColor: theme.colors.overlay,
    padding: theme.spacing.screenPadding,
  },
  container: {
    backgroundColor: theme.colors.black,
    flex: 1,
  },
  infoContainer: {
    backgroundColor: theme.colors.overlay,
    padding: theme.spacing.screenPadding,
  },
  infoText: {
    color: theme.colors.white,
    fontSize: theme.typography.sizes.body,
    marginBottom: theme.spacing.sm,
    textAlign: 'center',
  },
  noteText: {
    color: theme.colors.brass,
    fontSize: theme.typography.sizes.caption,
    fontStyle: 'italic',
    textAlign: 'center',
  },
  scannerContainer: {
    alignItems: 'center',
    flex: 1,
    justifyContent: 'center',
  },
  scannerPlaceholder: {
    alignItems: 'center',
    borderColor: theme.colors.brass,
    borderRadius: theme.borderRadius.qrCard,
    borderWidth: 2,
    height: 300,
    justifyContent: 'center',
    width: 300,
  },
  scannerPlaceholderText: {
    color: theme.colors.white,
    fontSize: theme.typography.sizes.body,
  },
});

export default QRScanner;
