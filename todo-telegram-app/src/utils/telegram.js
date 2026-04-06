export function initTelegramWebApp() {
  if (typeof window !== 'undefined' && window.Telegram?.WebApp) {
    const tg = window.Telegram.WebApp;
    tg.ready();
    tg.expand();
    return tg;
  }
  
  // Mock for development outside Telegram
  console.warn('Telegram WebApp not available, using mock data');
  return {
    initDataUnsafe: {
      user: {
        id: 123456789,
        first_name: 'Иван',
        last_name: 'Петров',
        username: 'ivan_p',
        phone_number: '+79991234567'
      }
    },
    ready: () => {},
    expand: () => {},
    MainButton: {
      text: 'Готово',
      onClick: () => {},
      show: () => {},
      hide: () => {}
    }
  };
}

export function getTelegramUser() {
  if (typeof window !== 'undefined' && window.Telegram?.WebApp?.initDataUnsafe?.user) {
    return window.Telegram.WebApp.initDataUnsafe.user;
  }
  return null;
}

export function sendToTelegramBot(data) {
  // In real app, send data to your backend which communicates with Telegram Bot API
  console.log('Sending to Telegram bot:', data);
  return Promise.resolve({ success: true });
}
