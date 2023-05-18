import React from 'react';
import styles from './ColdStartLoading.less';

export function ColdStartLoading(props: {
  prewarm: () => Promise<void>;
  children: React.ReactNode;
}) {
  const { prewarm, children } = props;
  const [isLoading, setIsLoading] = React.useState(true);
  const initialRef = React.useRef(false);

  React.useEffect(() => {
    if (!initialRef.current) {
      initialRef.current = true;
      prewarm().finally(() => {
        setIsLoading(false);
      });
    }
  }, [isLoading, prewarm]);

  return isLoading ? (
    <div className={styles.background}>
      <div
        // src="https://img.alicdn.com/imgextra/i4/O1CN018H1Ebb1MWTxEtS0tT_!!6000000001442-2-tps-1920-1080.png"
        className={styles['title-image']}
      />
      <div className={styles.loading} />
      <p className={styles.title}>
        Serverless 正在为您准备 AIGC 环境，AIGC 模型正在加载中
      </p>
      <p className={styles.subtitle}>
        注：频繁刷新可能会增加您的 GPU 消耗，喝杯咖啡耐心等待即可
      </p>
    </div>
  ) : (
    <div>{children}</div>
  );
}
