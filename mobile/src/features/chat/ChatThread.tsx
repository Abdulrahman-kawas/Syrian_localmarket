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
    backgroundColor: theme.colors.light.bg,
    flex: 1,
  },
  input: {
    backgroundColor: theme.colors.light.bgSunk,
    borderRadius: theme.borderRadius.button,
    color: theme.colors.light.text,
    flex: 1,
    fontSize: theme.typography.sizes.body,
    height: 50,
    marginRight: theme.spacing.md,
    paddingHorizontal: theme.spacing.lg,
  },
  inputContainer: {
    borderTopColor: theme.colors.light.line,
    borderTopWidth: 1,
    flexDirection: 'row',
    padding: theme.spacing.screenPadding,
  },
  messageBubble: {
    borderRadius: theme.borderRadius.button,
    paddingHorizontal: theme.spacing.lg,
    paddingVertical: theme.spacing.sm,
  },
  messageContainer: {
    marginBottom: theme.spacing.md,
    maxWidth: '80%',
  },
  messageList: {
    padding: theme.spacing.screenPadding,
  },
  messageText: {
    fontSize: theme.typography.sizes.body,
  },
  messageTime: {
    color: theme.colors.light.textSoft,
    fontSize: theme.typography.sizes.micro,
    marginTop: theme.spacing.xs,
    textAlign: 'right',
  },
  otherBubble: {
    backgroundColor: theme.colors.light.bgSunk,
  },
  otherMessage: {
    alignSelf: 'flex-start',
  },
  otherMessageText: {
    color: theme.colors.light.text,
  },
  ownBubble: {
    backgroundColor: theme.colors.pine,
  },
  ownMessage: {
    alignSelf: 'flex-end',
  },
  ownMessageText: {
    color: theme.colors.light.onPrimary,
  },
  sendButton: {
    alignItems: 'center',
    backgroundColor: theme.colors.pine,
    borderRadius: theme.borderRadius.button,
    height: 50,
    justifyContent: 'center',
    paddingHorizontal: theme.spacing.xl,
  },
  sendButtonText: {
    color: theme.colors.light.onPrimary,
    fontSize: theme.typography.sizes.body,
    fontWeight: theme.typography.weights.bold,
  },
});

export default ChatThread;
