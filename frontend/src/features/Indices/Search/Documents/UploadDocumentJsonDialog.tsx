import { Button, Dialog, DialogContent, Stack, Typography } from '@mui/material'
import { useFormik } from 'formik'
import { Fragment, FunctionComponent, useState } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import * as yup from 'yup'
import axiosInstance from '../../../../conf/axios'
import { showNotification } from '../../../Notification/notificationSlice'
import DeleteIcon from '@mui/icons-material/Delete'
import AttachmentIcon from '@mui/icons-material/Attachment'
import AddIcon from '@mui/icons-material/Add'
import { Publish } from '@mui/icons-material'
import { RootState } from '../../../../redux/store'


const UploadDocumentJsonDialog = () => {
    const index = useSelector((state: RootState) => state.indexSearch.index)

    const [open, setOpen] = useState(false)
    const [fileName, setFileName] = useState<string | undefined>(undefined)
    const [uploaded, setUploaded] = useState(true)

    const dispatch = useDispatch()

    const hideDialog = () => {
        setOpen(false)
    }
    const showDialog = () => {
        setOpen(true)
    }

    const validationSchema = yup.object().shape({
        file: yup.mixed().required('File is required'),
    })

    const formik = useFormik({
        initialValues: {
            file: undefined,
        },
        validationSchema,
        onSubmit: async (values) => {
            try {
                setUploaded(false)
                const formData = new FormData()
                formData.append('dataFile', values.file as any)

                const { data } = await axiosInstance.post(
                    `/indices/${index}/documents/files`,
                    formData,
                    {
                        headers: {
                            'Content-Type': 'multipart/form-docs',
                        },
                    }
                )

                if (data.success) {
                    dispatch(showNotification({ message: data.message }))
                    formik.resetForm()
                    setFileName(undefined)
                    hideDialog()
                } else {
                    dispatch(
                        showNotification({
                            message:
                                data.message ??
                                'Error while adding document, please try again later',
                            severity: 'error',
                            autohideSecs: 5
                        })
                    )
                }
            } catch (err: any) {
                dispatch(
                    showNotification({
                        message:
                            'Error while communicating with the server, please try again later',
                        severity: 'error',
                        autohideSecs: 5,
                    })
                )
            }
            setUploaded(true)
        },
    })

    const onFileUpload = (event: any) => {
        const file = event.currentTarget.files[0]
        if (file) {
            setFileName(file.name as string)
            formik.setFieldValue('file', file)
        }
    }

    const onClose = () => {
        
        hideDialog()
        setFileName(undefined)
        formik.resetForm()
    }

    const clearSelectedFile = () => {
        setFileName(undefined)
        formik.setFieldValue('file', undefined)
    }

    return (
        <Fragment>
            <Stack
                direction="row"
                justifyContent="flex-end"
                alignItems="center"
            >
                <Button
                    startIcon={<AttachmentIcon />}
                    variant="outlined"
                    color="secondary"
                    onClick={showDialog}
                >
                    Upload Documents in File
                </Button>
            </Stack>
            <Dialog open={open} fullWidth onClose={onClose} maxWidth="md">
                <Typography sx={{ ml: 2, mt: 2 }} variant="h5" fontWeight="600">
                    Upload Doucuments in File
                </Typography>
                <DialogContent>
                    <form onSubmit={formik.handleSubmit}>
                        {!fileName && (
                            <Button
                                variant="outlined"
                                color="secondary"
                                component="label"
                                startIcon={<AttachmentIcon />}
                            >
                                Select File
                                <input
                                    id="file"
                                    name="file"
                                    type="file"
                                    accept="application/json"
                                    hidden
                                    onChange={onFileUpload}
                                />
                            </Button>
                        )}
                        {fileName && (
                            <Fragment>
                                <Typography
                                    sx={{
                                        mr: 2,
                                        textOverflow: 'ellipsis',
                                        overflow: 'hidden',
                                    }}
                                    color="text.secondary"
                                    align="right"
                                >
                                    Selected File: {fileName}
                                </Typography>
                                <Stack
                                    direction="row"
                                    justifyContent="flex-end"
                                    alignItems="center"
                                >
                                    <Button
                                        sx={{ mb: 2, mt: 1 }}
                                        variant="outlined"
                                        size="small"
                                        endIcon={<DeleteIcon />}
                                        onClick={clearSelectedFile}
                                        disabled={!uploaded}
                                    >
                                        Remove Selection
                                    </Button>
                                </Stack>
                            </Fragment>
                        )}
                        <Stack
                            direction="row"
                            justifyContent="flex-end"
                            alignItems="center"
                        >
                            <Button
                                type="submit"
                                variant="contained"
                                disabled={!uploaded || !fileName}
                                startIcon={<Publish />}
                            >
                                Upload File
                            </Button>
                        </Stack>
                    </form>
                </DialogContent>
            </Dialog>
        </Fragment>
    )
}

export default UploadDocumentJsonDialog
