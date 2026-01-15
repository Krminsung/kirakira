import { useEffect } from 'react';

interface ConfirmModalProps {
    isOpen: boolean;
    onClose: () => void;
    onConfirm: () => void;
    title: string;
    message: string | React.ReactNode;
    confirmText?: string;
    cancelText?: string;
    type?: 'danger' | 'warning' | 'info';
}


export default function ConfirmModal({
    isOpen,
    onClose,
    onConfirm,
    title,
    message,
    confirmText = '확인',
    cancelText = '취소',
    type = 'info',
}: ConfirmModalProps) {

    useEffect(() => {
        if (isOpen) {
            document.body.style.overflow = 'hidden';
        } else {
            document.body.style.overflow = 'unset';
        }
        return () => {
            document.body.style.overflow = 'unset';
        };
    }, [isOpen]);

    if (!isOpen) return null;

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 animate-fadeIn">
            {/* Backdrop */}
            <div
                className="absolute inset-0 bg-black/60 backdrop-blur-sm"
                onClick={onClose}
            />

            {/* Modal */}
            <div className="relative bg-gradient-to-br from-gray-900 to-gray-800 rounded-2xl shadow-2xl border border-gray-700/50 max-w-md w-full p-6 animate-scaleIn">
                {/* Icon */}
                <div className="flex justify-center mb-4">
                    <div className={`w-16 h-16 rounded-full bg-gradient-to-br ${type === 'danger' ? 'from-red-500 to-pink-500' :
                            type === 'warning' ? 'from-yellow-500 to-orange-500' :
                                'from-indigo-500 to-pink-500'
                        } flex items-center justify-center`}>
                        {type === 'danger' || type === 'warning' ? (
                            <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                            </svg>
                        ) : (
                            <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                            </svg>
                        )}
                    </div>
                </div>


                {/* Title */}
                <h2 className="text-2xl font-bold text-center mb-3 bg-gradient-to-r from-indigo-400 to-pink-500 bg-clip-text text-transparent">
                    {title}
                </h2>

                {/* Message */}
                <div className="text-gray-300 text-center mb-6 leading-relaxed">
                    {typeof message === 'string' ? (
                        <p className="whitespace-pre-line">{message}</p>
                    ) : (
                        message
                    )}
                </div>


                {/* Buttons */}
                <div className="flex gap-3">
                    <button
                        onClick={onClose}
                        className="flex-1 px-4 py-3 bg-gray-700 hover:bg-gray-600 text-white rounded-lg transition-all transform hover:scale-105 active:scale-95 font-medium"
                    >
                        {cancelText}
                    </button>
                    <button
                        onClick={() => {
                            onConfirm();
                            onClose();
                        }}
                        className={`flex-1 px-4 py-3 bg-gradient-to-r ${type === 'danger' ? 'from-red-600 to-pink-600 hover:from-red-500 hover:to-pink-500' :
                                type === 'warning' ? 'from-yellow-600 to-orange-600 hover:from-yellow-500 hover:to-orange-500' :
                                    'from-indigo-600 to-pink-600 hover:from-indigo-500 hover:to-pink-500'
                            } text-white rounded-lg transition-all transform hover:scale-105 active:scale-95 font-medium shadow-lg`}
                    >
                        {confirmText}
                    </button>

                </div>
            </div>
        </div>
    );
}
