import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { Button } from '../../components';
import { theme } from '../../theme';

interface QRScannerProps {
  onScan: (code: string) => void;
  onCancel: () => void;
}

const QRScanner: React.FC<QRScannerProps> = ({ onScan, onCancel }) => {
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
          Scan the seller's QR code to purchase this product.
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
  container: {
    flex: 1,
    backgroundColor: '#000000',
  },
  scannerContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  scannerPlaceholder: {
    width: 300,
    height: 300,
    borderWidth: 2,
    borderColor: theme.colors.brass,
    borderRadius: theme.borderRadius.qrCard,
    justifyContent: 'center',
    alignItems: 'center',
  },
  scannerPlaceholderText: {
    fontSize: theme.typography.sizes.body,
    color: '#FFFFFF',
  },
  infoContainer: {
    padding: theme.spacing.screenPadding,
    backgroundColor: 'rgba(0,0,0,0.8)',
  },
  infoText: {
    fontSize: theme.typography.sizes.body,
    color: '#FFFFFF',
    textAlign: 'center',
    marginBottom: theme.spacing.sm,
  },
  noteText: {
    fontSize: theme.typography.sizes.caption,
    color: theme.colors.brass,
    textAlign: 'center',
    fontStyle: 'italic',
  },
  actions: {
    padding: theme.spacing.screenPadding,
    backgroundColor: 'rgba(0,0,0,0.8)',
  },
});

export default QRScanner;
