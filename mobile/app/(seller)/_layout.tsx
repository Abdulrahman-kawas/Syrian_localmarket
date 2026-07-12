import { Tabs } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import i18n from '../../src/i18n';
import { theme } from '../../src/theme';

export default function SellerLayout() {
  return (
    <Tabs
      screenOptions={{
        headerShown: true,
        tabBarActiveTintColor: theme.colors.light.primary,
        tabBarInactiveTintColor: theme.colors.light.textSoft,
      }}
    >
      <Tabs.Screen
        name="listings"
        options={{
          title: i18n.t('listings'),
          tabBarIcon: ({ color, size }) => <Ionicons name="list" color={color} size={size} />,
        }}
      />
      <Tabs.Screen
        name="create"
        options={{
          title: i18n.t('create'),
          tabBarIcon: ({ color, size }) => (
            <Ionicons name="add-circle" color={color} size={size} />
          ),
        }}
      />
      <Tabs.Screen
        name="chat"
        options={{
          title: i18n.t('chat'),
          tabBarIcon: ({ color, size }) => (
            <Ionicons name="chatbubbles" color={color} size={size} />
          ),
        }}
      />
    </Tabs>
  );
}
