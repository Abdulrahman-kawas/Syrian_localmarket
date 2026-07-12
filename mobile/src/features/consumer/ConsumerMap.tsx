import React from 'react';
import { View, StyleSheet } from 'react-native';
import MapView, { Marker } from 'react-native-maps';
import { theme } from '../../theme';

interface Seller {
  id: string;
  shopName: string;
  type: 'shop' | 'factory';
  latitude: number;
  longitude: number;
}

interface ConsumerMapProps {
  sellers: Seller[];
  onSellerPress: (seller: Seller) => void;
  onMapPress: (latitude: number, longitude: number) => void;
}

const ConsumerMap: React.FC<ConsumerMapProps> = ({
  sellers,
  onSellerPress,
  onMapPress,
}) => {
  return (
    <View style={styles.container}>
      <MapView
        style={styles.map}
        initialRegion={{
          latitude: 33.5138,
          longitude: 36.2765,
          latitudeDelta: 0.0922,
          longitudeDelta: 0.0421,
        }}
        onPress={(e) => {
          onMapPress(
            e.nativeEvent.coordinate.latitude,
            e.nativeEvent.coordinate.longitude,
          );
        }}
      >
        {sellers.map((seller) => (
          <Marker
            key={seller.id}
            coordinate={{
              latitude: seller.latitude,
              longitude: seller.longitude,
            }}
            title={seller.shopName}
            description={seller.type}
            onCalloutPress={() => onSellerPress(seller)}
          />
        ))}
      </MapView>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  map: {
    flex: 1,
  },
});

export default ConsumerMap;
