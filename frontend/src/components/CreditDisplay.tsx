import { useState, useEffect } from 'react';
import styles from './CreditDisplay.module.css';

interface CreditInfo {
    balance: number;
    max_balance: number;
    daily_free_amount: number;
    can_claim_daily: boolean;
    next_daily_claim: string | null;
    costs: {
        gemini_2_5_flash: number;
        gemini_3_flash: number;
        exaone: number;
        image_generation: number;
    };
}

export default function CreditDisplay() {
    const [creditInfo, setCreditInfo] = useState<CreditInfo | null>(null);
    const [claiming, setClaiming] = useState(false);

    const fetchCredits = async () => {
        try {
            const res = await fetch('/api/credits', {
                credentials: 'include'
            });
            if (res.ok) {
                const data = await res.json();
                setCreditInfo(data);
            }
        } catch (error) {
            console.error('Failed to fetch credits:', error);
        }
    };

    useEffect(() => {
        fetchCredits();
        // Refresh every 30 seconds
        const interval = setInterval(fetchCredits, 30000);
        return () => clearInterval(interval);
    }, []);

    const handleClaimDaily = async () => {
        setClaiming(true);
        try {
            const res = await fetch('/api/credits/daily', {
                method: 'POST',
                credentials: 'include'
            });

            if (res.ok) {
                const data = await res.json();
                alert(data.message);
                await fetchCredits();
            } else {
                const error = await res.json();
                alert(error.detail || 'Failed to claim daily credits');
            }
        } catch (error) {
            console.error('Failed to claim daily credits:', error);
            alert('Failed to claim daily credits');
            alert((error as any).detail || '일일 크레딧을 청구하지 못했습니다');
        } finally {
            setClaiming(false);
        }
    };

    if (!creditInfo) {
        return (
            <div className={styles.creditDisplay}>
                <div className={styles.loading}>로딩 중...</div>
            </div>
        );
    }

    return (
        <div className={styles.creditDisplay}>
            <div className={styles.balance}>
                <span className={styles.icon}>💎</span>
                <span className={styles.amount}>{creditInfo.balance}</span>
                <span className={styles.label}>키라</span>
            </div>

            {creditInfo.can_claim_daily && (
                <button
                    className={styles.claimButton}
                    onClick={handleClaimDaily}
                    disabled={claiming}
                >
                    {claiming ? '⏳' : '🎁'} 일일 {creditInfo.daily_free_amount} 키라 받기
                </button>
            )}

            <div className={styles.info}>
                <div className={styles.infoItem}>
                    <span>최대 보유량:</span>
                    <span>{creditInfo.max_balance} 💎</span>
                </div>
                <div className={styles.costs}>
                    <div className={styles.costItem}>
                        <span>Gemini 2.5:</span>
                        <span>{creditInfo.costs.gemini_2_5_flash} 💎</span>
                    </div>
                    <div className={styles.costItem}>
                        <span>Gemini 3:</span>
                        <span>{creditInfo.costs.gemini_3_flash} 💎</span>
                    </div>
                    <div className={styles.costItem}>
                        <span>EXAONE:</span>
                        <span>{creditInfo.costs.exaone} 💎</span>
                    </div>
                </div>
            </div>
        </div>
    );
}
