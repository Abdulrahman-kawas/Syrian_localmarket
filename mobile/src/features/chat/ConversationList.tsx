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
  avatar: {
    alignItems: 'center',
    backgroundColor: theme.colors.pine,
    borderRadius: 25,
    height: 50,
    justifyContent: 'center',
    marginRight: theme.spacing.md,
    width: 50,
  },
  avatarText: {
    color: theme.colors.light.onPrimary,
    fontSize: theme.typography.sizes.cardTitle,
    fontWeight: theme.typography.weights.extraBold,
  },
  card: {
    marginBottom: theme.spacing.md,
  },
  header: {
    alignItems: 'center',
    flexDirection: 'row',
  },
  info: {
    flex: 1,
  },
  list: {
    padding: theme.spacing.screenPadding,
  },
  message: {
    color: theme.colors.light.textSoft,
    fontSize: theme.typography.sizes.caption,
  },
  name: {
    color: theme.colors.light.text,
    fontSize: theme.typography.sizes.body,
    fontWeight: theme.typography.weights.bold,
    marginBottom: theme.spacing.xs,
  },
  time: {
    color: theme.colors.light.textSoft,
    fontSize: theme.typography.sizes.micro,
  },
});

export default ConversationList;
