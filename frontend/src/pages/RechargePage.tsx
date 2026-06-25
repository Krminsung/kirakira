import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

interface CreditInfo {
    balance: number;
    max_balance: number;
    daily_free_amount: number;
    can_claim_daily: boolean;
    next_daily_claim: string | null;
}

interface Transaction {
    id: string;
    amount: number;
    transaction_type: string;
    description: string;
    balance_after: number;
    created_at: string;
}

export default function RechargePage() {
    const navigate = useNavigate();
    const [creditInfo, setCreditInfo] = useState<CreditInfo | null>(null);
    const [transactions, setTransactions] = useState<Transaction[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchCreditInfo();
        fetchTransactions();
    }, []);

    const fetchCreditInfo = async () => {
        try {
            const res = await fetch('/api/credits', { credentials: 'include' });
            if (!res.ok) {
                navigate('/login');
                return;
            }
            const data = await res.json();
            setCreditInfo(data);
        } catch (error) {
            console.error('Failed to fetch credit info:', error);
        } finally {
            setLoading(false);
        }
    };

    const fetchTransactions = async () => {
        try {
            const res = await fetch('/api/credits/history', { credentials: 'include' });
            if (res.ok) {
                const data = await res.json();
                setTransactions(data.transactions || []);
            }
        } catch (error) {
            console.error('Failed to fetch transactions:', error);
        }
    };

    const handleClaimDaily = async () => {
        try {
            const res = await fetch('/api/credits/daily', {
                method: 'POST',
                credentials: 'include'
            });

            if (res.ok) {
                const data = await res.json();
                alert(data.message);
                fetchCreditInfo();
                fetchTransactions();
            } else {
                const error = await res.json();
                alert(error.detail || 'Failed to claim daily credits');
            }
        } catch (error) {
            console.error('Failed to claim daily credits:', error);
            alert('Failed to claim daily credits');
        }
    };

    const getTransactionIcon = (type: string) => {
        switch (type) {
            case 'signup': return '🎁';
            case 'daily': return '📅';
            case 'spend': return '💸';
            case 'earn': return '💰';
            default: return '💎';
        }
    };

    const getTransactionColor = (type: string) => {
        switch (type) {
            case 'signup':
            case 'daily':
            case 'earn':
                return 'text-green-400';
            case 'spend':
                return 'text-red-400';
            default:
                return 'text-gray-400';
        }
    };

    if (loading) {
        return (
            <div className="flex items-center justify-center min-h-[60vh]">
                <div className="w-12 h-12 border-4 border-indigo-600 border-t-transparent rounded-full animate-spin"></div>
            </div>
        );
    }

    return (
        <div className="py-8 max-w-4xl mx-auto">
            {/* Header */}
            <div className="mb-8">
                <h1 className="text-4xl font-bold bg-gradient-to-r from-indigo-400 to-pink-500 bg-clip-text text-transparent mb-2">
                    키라 충전하기
                </h1>
                <p className="text-gray-400">크레딧을 관리하고 사용 내역을 확인하세요</p>
            </div>

            {/* Credit Balance Card */}
            <div className="bg-gradient-to-br from-indigo-600 to-purple-600 p-8 rounded-xl mb-6 shadow-xl">
                <div className="flex items-center justify-between mb-6">
                    <div>
                        <p className="text-white/80 text-sm mb-2">현재 보유 크레딧</p>
                        <div className="flex items-center gap-3">
                            <span className="text-5xl">💎</span>
                            <span className="text-5xl font-bold text-white">{creditInfo?.balance || 0}</span>
                            <span className="text-2xl text-white/90">Kira</span>
                        </div>
                    </div>
                    <div className="text-right">
                        <p className="text-white/80 text-sm">최대 보유량</p>
                        <p className="text-2xl font-bold text-white">{creditInfo?.max_balance || 200} 💎</p>
                    </div>
                </div>

                {creditInfo?.can_claim_daily && (
                    <button
                        onClick={handleClaimDaily}
                        className="w-full bg-white/20 hover:bg-white/30 backdrop-blur-sm border-2 border-white/30 text-white font-bold py-4 px-6 rounded-xl transition-all transform hover:scale-105"
                    >
                        🎁 일일 무료 {creditInfo.daily_free_amount} 키라 받기
                    </button>
                )}
            </div>

            {/* Pricing Info */}
            <div className="bg-gradient-to-br from-gray-900 to-gray-800 p-6 rounded-xl border border-gray-700/50 mb-6 shadow-xl">
                <h2 className="text-2xl font-bold text-white mb-4 flex items-center gap-2">
                    <span>💰</span>
                    모델별 사용 비용
                </h2>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div className="bg-gray-800/50 p-4 rounded-lg border border-gray-700/30">
                        <div className="flex items-center justify-between mb-2">
                            <span className="text-gray-300">⚡ Gemini 2.5 Flash</span>
                            <span className="text-xl font-bold text-indigo-400">3 💎</span>
                        </div>
                        <p className="text-xs text-gray-500">메시지당</p>
                    </div>
                    <div className="bg-gray-800/50 p-4 rounded-lg border border-gray-700/30">
                        <div className="flex items-center justify-between mb-2">
                            <span className="text-gray-300">🚀 Gemini 3 Flash</span>
                            <span className="text-xl font-bold text-purple-400">5 💎</span>
                        </div>
                        <p className="text-xs text-gray-500">메시지당</p>
                    </div>
                    <div className="bg-gray-800/50 p-4 rounded-lg border border-gray-700/30">
                        <div className="flex items-center justify-between mb-2">
                            <span className="text-gray-300">🧠 EXAONE 236B</span>
                            <span className="text-xl font-bold text-green-400">1 💎</span>
                        </div>
                        <p className="text-xs text-gray-500">메시지당</p>
                    </div>
                </div>
                <div className="mt-4 bg-gray-800/50 p-4 rounded-lg border border-gray-700/30">
                    <div className="flex items-center justify-between">
                        <span className="text-gray-300">🎨 이미지 생성</span>
                        <span className="text-xl font-bold text-pink-400">10 💎</span>
                    </div>
                    <p className="text-xs text-gray-500 mt-2">이미지당</p>
                </div>
            </div>

            {/* Transaction History */}
            <div className="bg-gradient-to-br from-gray-900 to-gray-800 p-6 rounded-xl border border-gray-700/50 shadow-xl">
                <h2 className="text-2xl font-bold text-white mb-4 flex items-center gap-2">
                    <span>📊</span>
                    사용 내역
                </h2>
                {transactions.length > 0 ? (
                    <div className="space-y-2 max-h-96 overflow-y-auto">
                        {transactions.map((tx) => (
                            <div key={tx.id} className="bg-gray-800/30 p-4 rounded-lg border border-gray-700/20 hover:border-gray-600/50 transition-all">
                                <div className="flex items-center justify-between">
                                    <div className="flex items-center gap-3">
                                        <span className="text-2xl">{getTransactionIcon(tx.transaction_type)}</span>
                                        <div>
                                            <p className="text-white font-medium">{tx.description}</p>
                                            <p className="text-xs text-gray-500">
                                                {new Date(tx.created_at).toLocaleString('ko-KR')}
                                            </p>
                                        </div>
                                    </div>
                                    <div className="text-right">
                                        <p className={`text-lg font-bold ${getTransactionColor(tx.transaction_type)}`}>
                                            {tx.amount > 0 ? '+' : ''}{tx.amount} 💎
                                        </p>
                                        <p className="text-xs text-gray-500">잔액: {tx.balance_after} 💎</p>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                ) : (
                    <div className="text-center py-12">
                        <p className="text-gray-500 mb-2">아직 사용 내역이 없습니다</p>
                        <p className="text-sm text-gray-600">크레딧을 사용하면 여기에 표시됩니다</p>
                    </div>
                )}
            </div>
        </div>
    );
}
