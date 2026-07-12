import { useCallback, useEffect, useState } from 'react';
import { View, StyleSheet } from 'react-native';
import { useLocalSearchParams } from 'expo-router';
import { ChatThread } from '../../src/features/chat';
import { getMessages, sendMessage, type ThreadMessage } from '../../src/api/endpoints';
import { useAuthStore } from '../../src/store/authStore';
import { theme } from '../../src/theme';

export default function ChatThreadScreen() {
  const { id } = useLocalSearchParams<{ id: string }>();
  const currentUserId = useAuthStore((s) => s.user?.id ?? '');
  const [messages, setMessages] = useState<ThreadMessage[]>([]);

  const load = useCallback(async () => {
    try {
      setMessages(await getMessages(String(id)));
    } catch {
      setMessages([]);
    }
  }, [id]);

  useEffect(() => {
    load();
  }, [load]);

  async function onSend(content: string) {
    try {
      const msg = await sendMessage(String(id), content);
      setMessages((prev) => [...prev, msg]);
    } catch {
      // keep the composer contents; a toast could be added here
    }
  }

  return (
    <View style={styles.container}>
      <ChatThread messages={messages} currentUserId={currentUserId} onSendMessage={onSend} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { backgroundColor: theme.colors.light.bg, flex: 1 },
});
