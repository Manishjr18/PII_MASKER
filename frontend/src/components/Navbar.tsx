import styles from '../styles/navbar.module.css'

const Navbar = ({ theme, toggleTheme }: { theme: string; toggleTheme: () => void }) => {
  return (
    <div className={styles.navbar}>
      <div className={styles.navContent}>
        <div className={styles.logo}>🔐 PII Masker</div>
        <button className={styles.toggle} onClick={toggleTheme}>
          {theme === 'dark' ? '🌞' : '🌙'}
        </button>
      </div>
    </div>
  )
}

export default Navbar
