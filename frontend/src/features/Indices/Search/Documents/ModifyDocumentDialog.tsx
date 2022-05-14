import {
    Button,
    Dialog,
    DialogContent,
    DialogTitle,
    Stack,
    TextField,
} from '@mui/material'
import { useFormik } from 'formik'
import { Fragment, FunctionComponent, useEffect, useState } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import * as yup from 'yup'
import axiosInstance from '../../../../conf/axios'
import { RootState } from '../../../../redux/store'
import { showNotification } from '../../../Notification/notificationSlice'
import { DocumentDto } from '../../indexDtos'
import JSONInput from 'react-json-editor-ajrm'
import { localeEn } from '../../../Utils/JsonEditorLocale'
import SaveIcon from '@mui/icons-material/Save'
import AddCircleOutlineIcon from '@mui/icons-material/AddCircleOutline'
import EditIcon from '@mui/icons-material/Edit'
import { setDocument } from '../indexSearchSlice'

export interface ModifyDocumentDialogProps {
    variant: 'modify' | 'create'
    documentId?: string // used if the variant is 'modify'
}

const validationSchema = yup.object().shape({
    title: yup.string().optional().nullable(),
    text: yup.string().required(),
    additionalProperties: yup.object().optional().nullable(),
    id: yup.string().optional(),
})

const ModifyDocumentDialog: FunctionComponent<ModifyDocumentDialogProps> = ({
    variant,
    documentId,
}) => {
    const index = useSelector((state: RootState) => state.indexSearch.index)
    const [loading, setLoading] = useState(false)
    const [open, setOpen] = useState(false)
    const dispatch = useDispatch()

    // Creates configuration object for passed variant
    const createConfig = () => {
        if (variant === 'create') {
            return {
                title: 'Create document',
                variant: 'outlined' as 'outlined' | 'contained',
                color: 'primary',
                size: 'medium' as 'small' | 'medium' | 'large',
                apiSuccessMessage: 'New document was successfully added 😸',
            }
        }

        return {
            title: 'Modify document',
            variant: 'contained' as 'outlined' | 'contained',
            color: 'primary',
            size: 'small' as 'small' | 'medium' | 'large',
            apiSuccessMessage: 'Document was successfully modified 😸',
        }
    }

    const config = createConfig()

    // formik for form handling
    const formik = useFormik({
        initialValues: {
            title: '',
            text: '',
            additionalProperties: {},
            id: documentId,
        },
        validationSchema,
        onSubmit: async (values) => {
            let canCloseDialog = false
            try {
                const { data } = await axiosInstance.post(
                    `/indices/${index}/documents/${values.id ?? ''}`,
                    values
                )

                if (data.success) {
                    // if successful show notification and close dialog
                    dispatch(
                        showNotification({
                            message: config.apiSuccessMessage,
                            autohideSecs: 5,
                        })
                    )
                    canCloseDialog = true
                    // Set document values
                    dispatch(setDocument(data))
                } else {
                    // else show error notification and keep the dialog open
                    dispatch(
                        showNotification({
                            message:
                                data.message ??
                                'Error while adding document, please try again later',
                            severity: 'error',
                            autohideSecs: 5,
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

            // Close the dialog if its closeable
            if (canCloseDialog) {
                // Remove the form values as well since the dialog was successfuly submitted
                formik.resetForm()
                setOpen(false)
            }
        },
    })

    const onClose = () => {
        if (loading) {
            return
        }
        setOpen(false)
    }

    // Fetch the document if the variant is 'modify'
    useEffect(() => {
        setLoading(true)
        const fetchData = async () => {
            if (!open) {
                return
            }
            let keepDialogOpen = false
            try {
                const { data } = await axiosInstance.get(
                    `/indices/${index}/documents/${documentId}`
                )
                if (data.success) {
                    formik.setValues({ ...data.message })
                    keepDialogOpen = true
                } else {
                    dispatch(
                        showNotification({
                            message:
                                data.message ??
                                'An unknown error has occurred while fetching document 🤔, the document cannot be modified at the moment. 😥',
                            severity: 'error',
                            autohideSecs: 5,
                        })
                    )
                }
            } catch (err: any) {
                dispatch(showNotification({ message: err.message }))
            }

            if (!keepDialogOpen) {
                // If we got here it means that the document could not be fetched and we cannot modify it
                formik.resetForm()
                setOpen(false)
                return
            }

            setLoading(false)
        }
        if (variant === 'modify') {
            // We need to fetch the document
            fetchData()
        } else {
            setLoading(false)
        }
    }, [documentId, open, variant])

    return (
        <Fragment>
            <Button
                variant={config.variant}
                size={config.size}
                startIcon={variant === 'create' ? <AddCircleOutlineIcon /> : <EditIcon />}
                onClick={() => setOpen(true)}
            >
                {variant === 'create' ? 'Add New Document' : 'Modify'}
            </Button>
            <Dialog open={open} onClose={onClose}>
                <DialogTitle>
                    {variant === 'create' ? 'Add New Document' : 'Modify'}
                </DialogTitle>
                <DialogContent>
                    <form onSubmit={formik.handleSubmit}>
                        <TextField
                            label="Title"
                            name="title"
                            value={formik.values.title}
                            onChange={formik.handleChange}
                            onBlur={formik.handleBlur}
                            variant="outlined"
                            fullWidth
                            error={
                                formik.touched.title &&
                                Boolean(formik.errors.title)
                            }
                            helperText={
                                formik.touched.title && formik.errors.title
                            }
                            sx={{ mb: 2 }}
                        />
                        <TextField
                            label="Text"
                            name="text"
                            value={formik.values.text}
                            onChange={formik.handleChange}
                            onBlur={formik.handleBlur}
                            variant="outlined"
                            fullWidth
                            multiline
                            rows={5}
                            error={
                                formik.touched.text &&
                                Boolean(formik.errors.text)
                            }
                            helperText={
                                formik.touched.text && formik.errors.text
                            }
                            sx={{ mb: 2 }}
                        />
                        <TextField
                            label="id"
                            name="id"
                            value={formik.values.id}
                            onChange={formik.handleChange}
                            onBlur={formik.handleBlur}
                            variant="outlined"
                            fullWidth
                            error={
                                formik.touched.id && Boolean(formik.errors.id)
                            }
                            helperText={formik.touched.id && formik.errors.id}
                            sx={{ mb: 2 }}
                        />
                        <JSONInput
                            locale={localeEn}
                            // label="Additional properties"
                            // name="additionalProperties"
                            onChange={(val: any) => console.log(val)}
                            height="30vh"
                            width="100%"
                        />
                        <Stack alignItems="flex-end" sx={{ mt: 1 }}>
                            <Button
                                type="submit"
                                variant="contained"
                                color="primary"
                                startIcon={<SaveIcon />}
                            >
                                Save
                            </Button>
                        </Stack>
                    </form>
                </DialogContent>
            </Dialog>
        </Fragment>
    )
}

export default ModifyDocumentDialog
