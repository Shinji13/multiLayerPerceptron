import presetEnv from 'postcss-preset-env';
import autoprefixer from 'autoprefixer';

export default {
	plugins: [presetEnv({ stage: 1 }), autoprefixer()]
};
