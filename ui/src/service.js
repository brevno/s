import config from './config';

const createLink = async (url) => {
  try {
    const response = await fetch(`${config.backendApiUrl}/create`, {
      method: 'POST',
      body: JSON.stringify({ url: url }),
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error('Network response was not ok');
    }

    return await response.json();
  } catch (error) {
    console.error('Error creating link:', error);
    throw error;
  }
};

export { createLink };