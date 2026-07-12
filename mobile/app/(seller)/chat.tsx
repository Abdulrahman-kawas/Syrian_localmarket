import { useCallback, useState } from 'react';
import { View, Text, StyleSheet, ActivityIndicator } from 'react-native';
import { useFocusEffect, useRouter } from 'expo-router';
import { ConversationList } from '../../src/features/chat';
import { listConversations, type ConversationSummary } from '../../src/api/endpoints';
import { theme } from '../../src/theme';
import i18n from '../../src/i18n';

export default function SellerChatScreen() {
  const router = useRouter();
  const [conversations, setConversations] = useState<ConversationSummary[]>([]);
  const [loading, setLoading] = useState(true);

  const load = useCallback(async () => {
    try {
      setConversations(await listConversations());
    } catch {
      setConversations([]);
    } finally {
      setLoading(false);
    }
  }, []);

  useFocusEffect(
    useCallback(() => {
      load();
    }, [load]),
  );

  if (loading) {
    return (
      <View style={styles.center}>
        <ActivityIndicator size="large" color={theme.colors.light.primary} />
      </View>
    );
  }

  if (conversations.length === 0) {
    return (
      <View style={styles.center}>
        <Text style={styles.hint}>{i18n.t('noConversations')}</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <ConversationList
        conversations={conversations}
        onConversationPress={(c) => router.push(`/chat/${c.id}`)}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  center: {
    alignItems: 'center',
    backgroundColor: theme.colors.light.bg,
    flex: 1,
    justifyContent: 'center',
  },
  container: { backgroundColor: theme.colors.light.bg, flex: 1 },
  hint: { color: theme.colors.light.textSoft },
});
