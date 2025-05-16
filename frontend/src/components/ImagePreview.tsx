import { useEffect, useState } from 'react'
import styles from '../styles/preview.module.css'

type Props = {
  original: File | null
  masked: string | null
  loading: boolean
}

const ImagePreview = ({ original, masked, loading }: Props) => {
  const [originalUrl, setOriginalUrl] = useState('')

  useEffect(() => {
    if (original) {
      const url = URL.createObjectURL(original)
      setOriginalUrl(url)
      return () => URL.revokeObjectURL(url)
    }
  }, [original])

  const downloadImage = () => {
    if (!masked) return
    const a = document.createElement('a')
    a.href = masked
    a.download = 'masked_output.png'
    a.click()
  }

  return (
    <div className={styles.container}>
      {original && (
        <div>
          <p>📤 Uploaded</p>
          <img src={originalUrl} className={styles.image} />
        </div>
      )}
      {masked && !loading && (
        <div>
          <p>✅ Masked Output</p>
          <img src={masked} className={styles.image} />
          <button className={styles.download} onClick={downloadImage}>Download</button>
        </div>
      )}
    </div>
  )
}

export default ImagePreview
