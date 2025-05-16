import styles from '../styles/uploadForm.module.css'

type Props = {
  setFile: (file: File | null) => void
  onSubmit: () => void
  loading: boolean
}

const UploadForm = ({ setFile, onSubmit, loading }: Props) => {
  return (
    <div className={styles.card}>
      <input
        type="file"
        accept="image/*"
        onChange={(e) => e.target.files && setFile(e.target.files[0])}
        className={styles.input}
      />
      <button onClick={onSubmit} disabled={loading} className={styles.button}>
        {loading ? "Processing..." : "Upload & Mask"}
      </button>
    </div>
  )
}

export default UploadForm
