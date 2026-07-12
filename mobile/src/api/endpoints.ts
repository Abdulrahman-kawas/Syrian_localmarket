// Typed endpoint helpers that map backend (snake_case) payloads to the shapes
// the presentational feature components expect (camelCase).
import { api } from './client';

// --- Backend response shapes -------------------------------------------------
interface ApiSeller {
  id: string;
  user_id: string;
  shop_name: string;
  type: 'shop' | 'factory';
  phone?: string | null;
}

interface ApiProduct {
  id: string;
  seller_id: string;
  type: 'regular' | 'market_discount' | 'near_expiry';
  title: string;
  description: string | null;
  images: string[];
  original_price: number;
  discounted_price: number;
  currency: string;
  expiry_date: string | null;
  expiry_class: 'best_before' | 'use_by' | null;
  quantity: number;
  status: string;
  seller?: ApiSeller | null;
}

interface ApiPage<T> {
  items: T[];
  total: number;
  page: number;
  per_page: number;
}

interface ApiNearbySeller {
  id: string;
  shop_name: string;
  type: 'shop' | 'factory';
  geo_point: { type: 'Point'; coordinates: [number, number] } | null;
}

// --- Mappers -----------------------------------------------------------------
export interface FeedProduct {
  id: string;
  title: string;
  type: 'regular' | 'market_discount' | 'near_expiry';
  originalPrice: number;
  discountedPrice: number;
  expiryDate?: string;
  quantity: number;
  seller: { id: string; shopName: string };
}

export interface DetailProduct extends FeedProduct {
  description: string;
  expiryClass?: 'best_before' | 'use_by';
  images: string[];
  seller: { id: string; userId: string; shopName: string; phone: string };
}

function toFeedProduct(p: ApiProduct): FeedProduct {
  return {
    id: p.id,
    title: p.title,
    type: p.type,
    originalPrice: Number(p.original_price),
    discountedPrice: Number(p.discounted_price),
    expiryDate: p.expiry_date ?? undefined,
    quantity: p.quantity,
    seller: { id: p.seller?.id ?? p.seller_id, shopName: p.seller?.shop_name ?? '' },
  };
}

function toDetailProduct(p: ApiProduct): DetailProduct {
  return {
    ...toFeedProduct(p),
    description: p.description ?? '',
    expiryClass: p.expiry_class ?? undefined,
    images: p.images ?? [],
    seller: {
      id: p.seller?.id ?? p.seller_id,
      userId: p.seller?.user_id ?? '',
      shopName: p.seller?.shop_name ?? '',
      phone: p.seller?.phone ?? '',
    },
  };
}

// --- Endpoints ---------------------------------------------------------------
export interface ProductQuery {
  lat?: number;
  lng?: number;
  radius?: number;
  type?: string;
  sort?: string;
}

export async function listProducts(q: ProductQuery = {}): Promise<FeedProduct[]> {
  const params = new URLSearchParams();
  Object.entries(q).forEach(([k, v]) => {
    if (v !== undefined && v !== null) params.append(k, String(v));
  });
  const qs = params.toString();
  const res = await api.get<ApiPage<ApiProduct>>(`/products${qs ? `?${qs}` : ''}`);
  return res.items.map(toFeedProduct);
}

export async function getProduct(id: string): Promise<DetailProduct> {
  const p = await api.get<ApiProduct>(`/products/${id}`);
  return toDetailProduct(p);
}

export async function createProduct(data: {
  title: string;
  description: string;
  type: string;
  originalPrice: number;
  discountedPrice: number;
  expiryDate?: string;
  expiryClass?: string;
  quantity: number;
}): Promise<DetailProduct> {
  const p = await api.post<ApiProduct>('/products', {
    title: data.title,
    description: data.description,
    type: data.type,
    original_price: data.originalPrice,
    discounted_price: data.discountedPrice,
    expiry_date: data.expiryDate,
    expiry_class: data.expiryClass,
    quantity: data.quantity,
  });
  return toDetailProduct(p);
}

export async function myListings(): Promise<FeedProduct[]> {
  // Sellers see their own active + inactive listings via the products list
  // filtered client-side is not ideal; the backend returns active listings.
  const res = await api.get<ApiPage<ApiProduct>>('/products?per_page=100');
  return res.items.map(toFeedProduct);
}

export async function nearbySellers(
  lat: number,
  lng: number,
  radius = 5,
): Promise<Array<{ id: string; shopName: string; type: 'shop' | 'factory'; latitude: number; longitude: number }>> {
  const res = await api.get<{ sellers: ApiNearbySeller[] }>(
    `/maps/nearby?lat=${lat}&lng=${lng}&radius=${radius}`,
  );
  return res.sellers
    .filter((s) => s.geo_point)
    .map((s) => ({
      id: s.id,
      shopName: s.shop_name,
      type: s.type,
      latitude: s.geo_point!.coordinates[1],
      longitude: s.geo_point!.coordinates[0],
    }));
}

export async function scanQr(code: string): Promise<{ transactionId: string; status: string }> {
  const res = await api.post<{ transaction_id: string; status: string }>('/qr/scan', { code });
  return { transactionId: res.transaction_id, status: res.status };
}

export interface ThreadMessage {
  id: string;
  senderId: string;
  content: string;
  createdAt: string;
}

export async function updateLocation(lat: number, lng: number): Promise<void> {
  await api.put('/users/me/location', { latitude: lat, longitude: lng });
}

export async function createConversation(participantId: string): Promise<{ id: string }> {
  const res = await api.post<{ id: string }>('/conversations', {
    participant_id: participantId,
  });
  return { id: res.id };
}

export interface ConversationSummary {
  id: string;
  participant: { id: string; name: string };
  lastMessage: string;
  lastMessageTime: string;
}

export async function listConversations(): Promise<ConversationSummary[]> {
  const items = await api.get<
    Array<{
      id: string;
      participant: { id: string; name: string };
      last_message: string;
      last_message_time: string;
    }>
  >('/conversations');
  return items.map((c) => ({
    id: c.id,
    participant: c.participant,
    lastMessage: c.last_message,
    lastMessageTime: c.last_message_time,
  }));
}

export async function getMessages(conversationId: string): Promise<ThreadMessage[]> {
  const res = await api.get<{
    items: Array<{ id: string; sender_id: string; content: string; created_at: string }>;
  }>(`/conversations/${conversationId}/messages`);
  return res.items.map((m) => ({
    id: m.id,
    senderId: m.sender_id,
    content: m.content,
    createdAt: m.created_at,
  }));
}

export async function sendMessage(conversationId: string, content: string): Promise<ThreadMessage> {
  const m = await api.post<{ id: string; sender_id: string; content: string; created_at: string }>(
    `/conversations/${conversationId}/messages`,
    { content },
  );
  return { id: m.id, senderId: m.sender_id, content: m.content, createdAt: m.created_at };
}
