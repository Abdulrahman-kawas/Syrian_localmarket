import React from 'react';
import { View, Text, StyleSheet, FlatList, TouchableOpacity } from 'react-native';
import { Card } from '../../components';
import { theme } from '../../theme';

interface Conversation {
  id: string;
  participant: {
    id: string;
    name: string;
  };
  lastMessage: string;
  lastMessageTime: string;
}

interface ConversationListProps {
  conversations: Conversation[];
  onConversationPress: (conversation: Conversation) => void;
}

const ConversationList: React.FC<ConversationListProps> = ({
  conversations,
  onConversationPress,
}) => {
  const renderConversation = ({ item }: { item: Conversation }) => (
    <TouchableOpacity onPress={() => onConversationPress(item)}>
      <Card style={styles.card}>
        <View style={styles.header}>
          <View style={styles.avatar}>
            <Text style={styles.avatarText}>
              {item.participant.name.charAt(0)}
            </Text>
          </View>
          <View style={styles.info}>
            <Text style={styles.name}>{item.participant.name}</Text>
            <Text style={styles.message} numberOfLines={1}>
              {item.lastMessage}
            </Text>
          </View>
          <Text style={styles.time}>{item.lastMessageTime}</Text>
        </View>
      </Card>
    </TouchableOpacity>
  );

  return (
    <FlatList
      data={conversations}
      renderItem={renderConversation}
      keyExtractor={(item) => item.id}
      contentContainerStyle={styles.list}
    />
  );
};

const styles = StyleSheet.create({
  list: {
    padding: theme.spacing.screenPadding,
  },
  card: {
    marginBottom: theme.spacing.md,
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  avatar: {
    width: 50,
    height: 50,
    borderRadius: 25,
    backgroundColor: theme.colors.pine,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: theme.spacing.md,
  },
  avatarText: {
    fontSize: theme.typography.sizes.cardTitle,
    fontWeight: theme.typography.weights.extraBold,
    color: theme.colors.light.onPrimary,
  },
  info: {
    flex: 1,
  },
  name: {
    fontSize: theme.typography.sizes.body,
    fontWeight: theme.typography.weights.bold,
    color: theme.colors.light.text,
    marginBottom: theme.spacing.xs,
  },
  message: {
    fontSize: theme.typography.sizes.caption,
    color: theme.colors.light.textSoft,
  },
  time: {
    fontSize: theme.typography.sizes.micro,
    color: theme.colors.light.textSoft,
  },
});

export default ConversationList;
