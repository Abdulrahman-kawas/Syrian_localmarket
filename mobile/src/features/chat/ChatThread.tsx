import React, { useState } from 'react';
import { View, Text, StyleSheet, FlatList, TextInput, TouchableOpacity } from 'react-native';
import { theme } from '../../theme';

interface Message {
  id: string;
  senderId: string;
  content: string;
  createdAt: string;
}

interface ChatThreadProps {
  messages: Message[];
  currentUserId: string;
  onSendMessage: (content: string) => void;
}

const ChatThread: React.FC<ChatThreadProps> = ({
  messages,
  currentUserId,
  onSendMessage,
}) => {
  const [inputText, setInputText] = useState('');

  const handleSend = () => {
    if (inputText.trim()) {
      onSendMessage(inputText.trim());
      setInputText('');
    }
  };

  const renderMessage = ({ item }: { item: Message }) => {
    const isOwnMessage = item.senderId === currentUserId;

    return (
      <View
        style={[
          styles.messageContainer,
          isOwnMessage ? styles.ownMessage : styles.otherMessage,
        ]}
      >
        <View
          style={[
            styles.messageBubble,
            isOwnMessage ? styles.ownBubble : styles.otherBubble,
          ]}
        >
          <Text
            style={[
              styles.messageText,
              isOwnMessage ? styles.ownMessageText : styles.otherMessageText,
            ]}
          >
            {item.content}
          </Text>
        </View>
        <Text style={styles.messageTime}>{item.createdAt}</Text>
      </View>
    );
  };

  return (
    <View style={styles.container}>
      <FlatList
        data={messages}
        renderItem={renderMessage}
        keyExtractor={(item) => item.id}
        contentContainerStyle={styles.messageList}
      />

      <View style={styles.inputContainer}>
        <TextInput
          style={styles.input}
          value={inputText}
          onChangeText={setInputText}
          placeholder="Type a message..."
          placeholderTextColor={theme.colors.light.textSoft}
        />
        <TouchableOpacity style={styles.sendButton} onPress={handleSend}>
          <Text style={styles.sendButtonText}>Send</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: theme.colors.light.bg,
  },
  messageList: {
    padding: theme.spacing.screenPadding,
  },
  messageContainer: {
    marginBottom: theme.spacing.md,
    maxWidth: '80%',
  },
  ownMessage: {
    alignSelf: 'flex-end',
  },
  otherMessage: {
    alignSelf: 'flex-start',
  },
  messageBubble: {
    paddingHorizontal: theme.spacing.lg,
    paddingVertical: theme.spacing.sm,
    borderRadius: theme.borderRadius.button,
  },
  ownBubble: {
    backgroundColor: theme.colors.pine,
  },
  otherBubble: {
    backgroundColor: theme.colors.light.bgSunk,
  },
  messageText: {
    fontSize: theme.typography.sizes.body,
  },
  ownMessageText: {
    color: theme.colors.light.onPrimary,
  },
  otherMessageText: {
    color: theme.colors.light.text,
  },
  messageTime: {
    fontSize: theme.typography.sizes.micro,
    color: theme.colors.light.textSoft,
    marginTop: theme.spacing.xs,
    textAlign: 'right',
  },
  inputContainer: {
    flexDirection: 'row',
    padding: theme.spacing.screenPadding,
    borderTopWidth: 1,
    borderTopColor: theme.colors.light.line,
  },
  input: {
    flex: 1,
    height: 50,
    backgroundColor: theme.colors.light.bgSunk,
    borderRadius: theme.borderRadius.button,
    paddingHorizontal: theme.spacing.lg,
    fontSize: theme.typography.sizes.body,
    color: theme.colors.light.text,
    marginRight: theme.spacing.md,
  },
  sendButton: {
    height: 50,
    paddingHorizontal: theme.spacing.xl,
    backgroundColor: theme.colors.pine,
    borderRadius: theme.borderRadius.button,
    justifyContent: 'center',
    alignItems: 'center',
  },
  sendButtonText: {
    fontSize: theme.typography.sizes.body,
    fontWeight: theme.typography.weights.bold,
    color: theme.colors.light.onPrimary,
  },
});

export default ChatThread;
