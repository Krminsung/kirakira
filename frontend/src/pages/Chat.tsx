import { useState, useEffect, useRef } from "react";
import { useNavigate, useParams, Link, useSearchParams } from "react-router-dom";
import styles from "./Chat.module.css";
import ChatSidebar from "../components/ChatSidebar";

interface Character {
    id: string;
    name: string;
    profileImage: string | null;
    greeting: string;
}

interface Message {
    id: string;
    role: "USER" | "ASSISTANT" | "MODEL";
    content: string;
    createdAt: string;
}

export default function Chat() {
    const { id } = useParams<{ id: string }>();
    const navigate = useNavigate();
    const [searchParams, setSearchParams] = useSearchParams();
    const messagesEndRef = useRef<HTMLDivElement>(null);
    const [user, setUser] = useState<any>(null);

    const [character, setCharacter] = useState<Character | null>(null);
    const [messages, setMessages] = useState<Message[]>([]);
    const [input, setInput] = useState("");
    const [loading, setLoading] = useState(true);
    const [sending, setSending] = useState(false);
    const [conversationId, setConversationId] = useState<string | null>(searchParams.get("conversationId"));
    const [streamingContent, setStreamingContent] = useState("");
    const [selectedModel, setSelectedModel] = useState("gemini-2.5-flash");
    const [creditError, setCreditError] = useState<string | null>(null);

    // Conversation sidebar state
    const [conversations, setConversations] = useState<any[]>([]);
    const [sidebarOpen] = useState(true);

    // Sync conversationId with URL params when they change
    useEffect(() => {
        const convId = searchParams.get("conversationId");
        console.log(`[Chat] URL conversationId changed to: ${convId}`);
        setConversationId(convId);
    }, [searchParams]);

    // Fetch conversations
    const fetchConversations = async () => {
        try {
            const res = await fetch('/api/conversations/');

            if (res.ok) {
                const data = await res.json();
                setConversations(data.conversations || []);
            }
        } catch (error) {
            console.error('Failed to fetch conversations:', error);
        }
    };

    useEffect(() => {
        if (user) {
            fetchConversations();
        }
    }, [user]);

    useEffect(() => {
        fetch('/api/auth/me')
            .then(res => {
                if (res.ok) return res.json();
                throw new Error('Unauthorized');
            })
            .then(data => setUser(data.user))
            .catch(() => navigate('/login'));
    }, [navigate]);

    useEffect(() => {
        async function fetchCharacter() {
            try {
                const res = await fetch(`/api/characters/${id}`);
                const data = await res.json();

                if (res.ok) {
                    setCharacter(data.character);
                    // Only set greeting message if this is a NEW conversation (no conversationId)
                    if (messages.length === 0 && !conversationId) {
                        setMessages([
                            {
                                id: "greeting",
                                role: "ASSISTANT",
                                content: data.character.greeting.replace(
                                    /\{\{user\}\}/g,
                                    user?.name || "User"
                                ),
                                createdAt: new Date().toISOString(),
                            },
                        ]);
                    }
                }
            } catch (error) {
                console.error("Failed to fetch character:", error);
            } finally {
                setLoading(false);
            }
        }

        if (user) {
            fetchCharacter();
        }
    }, [user, id]);

    // Load messages if conversationId exists
    useEffect(() => {
        async function fetchMessages() {
            if (!conversationId) {
                console.log('[Chat] No conversationId, skipping message fetch');
                return;
            }

            console.log(`[Chat] Fetching messages for conversation: ${conversationId}`);
            try {
                const res = await fetch(`/api/chat/${conversationId}/messages`);
                if (res.ok) {
                    const data = await res.json();
                    console.log(`[Chat] Loaded ${data.messages?.length || 0} messages`);
                    setMessages(data.messages || []);
                } else {
                    console.error(`[Chat] Failed to fetch messages: ${res.status}`);
                }
            } catch (error) {
                console.error("[Chat] Failed to fetch messages:", error);
            }
        }

        if (conversationId) {
            fetchMessages();
        }
    }, [conversationId]);


    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [messages, streamingContent]);

    const sendMessage = async (e?: React.FormEvent) => {
        if (e) e.preventDefault();
        if (!input.trim() || sending) return;

        const userMessage = input.trim();
        setInput("");
        setSending(true);
        setStreamingContent("");

        // Add user message
        const newUserMessage: Message = {
            id: Date.now().toString(),
            role: "USER",
            content: userMessage,
            createdAt: new Date().toISOString(),
        };
        setMessages((prev) => [...prev, newUserMessage]);

        try {
            const res = await fetch("/api/chat/", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    characterId: id,
                    message: userMessage,
                    conversationId,
                    model: selectedModel,
                }),
            });

            console.log(`[Chat] Sent message with conversationId: ${conversationId}`);

            if (!res.ok) {
                const errorData = await res.json();
                if (res.status === 402) {
                    setCreditError(errorData.detail || "Insufficient credits");
                    setMessages((prev) => prev.filter((m: any) => m.id !== newUserMessage.id));
                    setSending(false);
                    return;
                }
                throw new Error(errorData.detail || errorData.error || "Failed to send message");
            }

            setCreditError(null);

            const reader = res.body?.getReader();
            const decoder = new TextDecoder();
            let fullContent = "";

            if (reader) {
                while (true) {
                    const { done, value } = await reader.read();
                    if (done) break;

                    const chunk = decoder.decode(value);
                    const lines = chunk.split("\n");

                    for (const line of lines) {
                        if (line.startsWith("data: ")) {
                            try {
                                const data = JSON.parse(line.slice(6));
                                if (data.text) {
                                    fullContent += data.text;
                                    setStreamingContent(fullContent);
                                }
                                if (data.conversationId && data.conversationId !== conversationId) {
                                    console.log(`[Chat] Received conversationId: ${data.conversationId}`);
                                    setConversationId(data.conversationId);
                                    setSearchParams({ conversationId: data.conversationId }, { replace: true });
                                    fetchConversations();
                                }
                                if (data.done) {
                                    console.log(`[Chat] Stream done`);
                                    fetchConversations();
                                }

                            } catch {
                                // Ignore parse errors
                            }
                        }
                    }
                }
            }

            // Add assistant message
            const assistantMessage: Message = {
                id: Date.now().toString() + "-assistant",
                role: "ASSISTANT",
                content: fullContent,
                createdAt: new Date().toISOString(),
            };
            setMessages((prev) => [...prev, assistantMessage]);
            setStreamingContent("");
        } catch (error) {
            console.error("Chat error:", error);
            setMessages((prev) => prev.filter((m) => m.id !== newUserMessage.id));
        } finally {
            setSending(false);
        }
    };

    const handleRegenerateImage = async (messageId: string) => {
        if (sending) return;

        try {
            setSending(true);

            // First, delete from DB if conversationId exists
            if (conversationId) {
                try {
                    const response = await fetch(`/api/chat/messages/${messageId}`, {
                        method: 'DELETE',
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    });

                    if (!response.ok) {
                        console.error('Failed to delete message from DB:', await response.text());
                    }
                } catch (err) {
                    console.error('Failed to delete old message:', err);
                }
            }

            // Remove old image message from UI
            setMessages(prev => prev.filter(msg => msg.id !== messageId));

            // Wait a bit to ensure deletion is processed
            await new Promise(resolve => setTimeout(resolve, 300));

            // Generate new image
            await handleGenerateImage();
        } catch (error) {
            console.error('Regenerate error:', error);
            alert('이미지 재생성에 실패했습니다.');
        } finally {
            setSending(false);
        }
    };

    const handleGenerateImage = async () => {
        if (sending) return;

        const tempId = Date.now().toString();
        // Add loading message
        setMessages(prev => [...prev, {
            id: tempId,
            role: "ASSISTANT",
            content: "🎨 그림을 그리고 있습니다...",
            createdAt: new Date().toISOString()
        }]);

        try {
            const res = await fetch("/api/chat/image", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    messages: messages,
                    characterName: character?.name || "Character",
                    conversationId: conversationId
                })
            });

            if (!res.ok) throw new Error("Failed");

            const data = await res.json();

            // Replace loading message with image
            setMessages(prev => prev.map(msg =>
                msg.id === tempId
                    ? {
                        ...msg,
                        content: `![Scene](${data.imageUrl})`
                    }
                    : msg
            ));

        } catch (error) {
            setMessages(prev => prev.filter(msg => msg.id !== tempId));
            alert("이미지 생성에 실패했습니다.");
        }
    };

    if (loading) {

        return (
            <div className={styles.loading}>
                <div className="spinner" />
            </div>
        );
    }

    if (!character) {
        return (
            <div className={styles.error}>
                <p>캐릭터를 찾을 수 없습니다.</p>
            </div>
        );
    }

    return (
        <div className="flex h-screen bg-gray-900">
            {/* Chat Sidebar */}
            {sidebarOpen && (
                <ChatSidebar
                    conversations={conversations}
                    activeConversationId={conversationId || undefined}
                    onConversationSelect={(convId) => {
                        // Find the conversation to get its character ID
                        const conversation = conversations.find(c => c.id === convId);
                        if (conversation) {
                            // Navigate to the character's chat page with the conversation ID
                            navigate(`/characters/${conversation.character.id}/chat?conversationId=${convId}`);
                        }
                    }}

                    onConversationDelete={() => {
                        fetchConversations();
                    }}
                    onRefresh={fetchConversations}
                />
            )}

            {/* Main Chat Area */}
            <div className={`flex-1 flex flex-col ${styles.container}`}>
                <div className={styles.header}>
                    <Link to={`/characters/${id}`} className={styles.backButton}>
                        ←
                    </Link>
                    <div className={styles.headerInfo}>
                        <h1>{character?.name}</h1>
                        <span className={styles.status}>Online</span>
                    </div>
                    <select
                        className={styles.modelSelect}
                        value={selectedModel}
                        onChange={(e: any) => setSelectedModel(e.target.value)}
                        disabled={sending}
                    >
                        <option value="gemini-2.5-flash">⚡ 2.5 Flash (3💎)</option>
                        <option value="gemini-3-flash">🚀 3.0 Flash (5💎)</option>
                        <option value="exaone-236b">🧠 EXAONE 236B (1💎)</option>
                        <option value="cukee-ai">🍪 Cukee AI (1💎)</option>
                    </select>
                    <button
                        onClick={handleGenerateImage}
                        disabled={sending}
                        className={styles.imageBtn}
                        title="현재 상황 그리기"
                    >
                        🎨
                    </button>
                </div>

                {creditError && (
                    <div className={styles.usageError}>
                        ⚠️ {creditError}
                    </div>
                )}

                <div className={styles.messages}>
                    {messages.map((msg) => (
                        <div
                            key={msg.id}
                            className={`${styles.message} ${msg.role === "USER" ? styles.userMessage : styles.modelMessage
                                }`}
                        >
                            {(msg.role === "ASSISTANT" || msg.role === "MODEL") && (
                                <div className={styles.avatar}>
                                    {character?.profileImage ? (
                                        <img
                                            src={character.profileImage}
                                            alt={character.name}
                                            width={40}
                                            height={40}
                                            className={styles.avatarImg}
                                        />
                                    ) : (
                                        character?.name[0]
                                    )}
                                </div>
                            )}
                            <div className={styles.bubble}>
                                {msg.content.startsWith("![Scene]") ? (
                                    <div className={styles.generatedImage}>
                                        <img
                                            src={msg.content.match(/\((.*?)\)/)?.[1] || ""}
                                            alt="Generated Scene"
                                            style={{ width: '100%', height: 'auto', borderRadius: '8px' }}
                                        />
                                        <button
                                            onClick={() => handleRegenerateImage(msg.id)}
                                            disabled={sending}
                                            className={styles.regenerateBtn}
                                            title="다시 그리기"
                                        >
                                            🔄 다시 그리기
                                        </button>
                                    </div>
                                ) : (
                                    msg.content
                                )}
                            </div>
                        </div>
                    ))}

                    {sending && !streamingContent && (
                        <div className={`${styles.message} ${styles.modelMessage}`}>
                            <div className={styles.avatar}>
                                {character?.profileImage ? (
                                    <img
                                        src={character.profileImage}
                                        alt={character.name}
                                        className={`${styles.avatarImg} w-10 h-10 object-cover rounded-full`}
                                    />
                                ) : (
                                    character?.name[0]
                                )}
                            </div>
                            <div className={styles.bubble}>
                                <div className={styles.typing}>
                                    <span></span>
                                    <span></span>
                                    <span></span>
                                </div>
                            </div>
                        </div>
                    )}

                    {streamingContent && (
                        <div className={`${styles.message} ${styles.modelMessage}`}>
                            <div className={styles.avatar}>
                                {character?.profileImage ? (
                                    <img
                                        src={character.profileImage}
                                        alt={character.name}
                                        className={`${styles.avatarImg} w-10 h-10 object-cover rounded-full`}
                                    />
                                ) : (
                                    character?.name[0]
                                )}
                            </div>
                            <div className={styles.bubble}>
                                {streamingContent}
                            </div>
                        </div>
                    )}
                    <div ref={messagesEndRef} />
                </div>

                <form onSubmit={sendMessage} className={styles.inputForm}>
                    <input
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        placeholder="메시지를 입력하세요..."
                        className={styles.input}
                        disabled={sending}
                    />
                    <button type="submit" className={styles.sendBtn} disabled={sending || !input.trim()}>
                        전송
                    </button>
                </form>
            </div>
        </div>
    );
}
