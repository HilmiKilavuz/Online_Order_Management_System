// Load environment variables from .env file
(async function loadEnv() {
    try {
        const response = await fetch('/.env');
        const text = await response.text();
        const env = {};

        text.split('\n').forEach(line => {
            line = line.trim();
            if (line && !line.startsWith('#')) {
                const [key, ...valueParts] = line.split('=');
                env[key.trim()] = valueParts.join('=').trim();
            }
        });

        window.ENV = env;
    } catch (error) {
        console.warn('Could not load .env file, using defaults');
        window.ENV = {};
    }
})();
