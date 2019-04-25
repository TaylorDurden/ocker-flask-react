import React from 'react';
import styles from './index.less'; // 按照 CSS Modules 的方式引入样式文件。

export default ({ src, desc, style }) => (
  <div style={style} className={styles.imageWrapper}>
    <img src={src} alt={desc} className={styles.img} />
    {desc && <div className={styles.desc}>{desc}</div>}
  </div>
);
