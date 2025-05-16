import { useEffect, useState } from 'react'
import styles from './styles/landing.module.css'
import Navbar from './components/Navbar'

const App = () => {
  const [original, setOriginal] = useState<File | null>(null)
  const [maskedUrl, setMaskedUrl] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)
  const [theme, setTheme] = useState('dark')

  

  const toggleTheme = () => {
    const newTheme = theme === 'dark' ? 'light' : 'dark'
    setTheme(newTheme)
    document.documentElement.className = newTheme
  }

  useEffect(() => {
  document.documentElement.setAttribute("data-theme", theme)
}, [theme])


  const handleUpload = async () => {
    if (!original) return alert("Please upload an image.")
    const formData = new FormData()
    formData.append('file', original)

    setLoading(true)
    setMaskedUrl(null)

    try {
      const res = await fetch('http://localhost:8000/upload/', {
        method: 'POST',
        body: formData
      })
      const blob = await res.blob()
      const url = URL.createObjectURL(blob)
      setMaskedUrl(url)
    } catch {
      alert("Something went wrong.")
    } finally {
      setLoading(false)
    }
  }

  const downloadImage = () => {
    if (!maskedUrl) return
    const a = document.createElement('a')
    a.href = maskedUrl
    a.download = 'masked_output.png'
    a.click()
  }

  return (
    <div className={styles.container}>
      <Navbar theme={theme} toggleTheme={toggleTheme} />

      <div className={styles.header}>
        <h1>PII Masking Tool</h1>
        <h3>Automatically detect & mask sensitive info from ID cards</h3>
      </div>

      <div className={styles.uploadBox}>
        <input
          type="file"
          accept="image/png, image/jpeg"
          onChange={(e) => {
            if (e.target.files) {
              setOriginal(e.target.files[0])
              setMaskedUrl(null)
            }
          }}
        />
        <p className={styles.note}>*Upload only JPG and PNG (no other formats supported)</p>
        <button className={styles.button} onClick={handleUpload} disabled={loading}>
          {loading ? 'Processing...' : 'Upload & Mask'}
        </button>
      </div>

      {(original || maskedUrl) && (
        <div className={styles.previewSection}>
          {original && (
            <div className={styles.previewCard}>
              <p>📤 Uploaded</p>
              <img
                src={URL.createObjectURL(original)}
                className={styles.previewImage}
              />
            </div>
          )}

          {maskedUrl && !loading && (
            <div className={styles.previewCard}>
              <p>✅ Masked</p>
              <img src={maskedUrl} className={styles.previewImage} />
              <button className={styles.downloadIcon} onClick={downloadImage}>
                ⬇️
              </button>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default App
