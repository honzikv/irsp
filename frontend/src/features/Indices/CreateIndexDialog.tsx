import { ChangeEvent, Fragment, FunctionComponent, useEffect, useState } from 'react'
import Dialog, { DialogProps } from '@mui/material/Dialog'
import {
    Button,
    Checkbox,
    DialogContent,
    Divider,
    FormControl,
    FormControlLabel,
    FormGroup,
    InputLabel,
    MenuItem,
    Stack,
    TextField,
    Typography,
} from '@mui/material'
import { useFormik } from 'formik'
import * as yup from 'yup'
import Select, { SelectChangeEvent } from '@mui/material/Select'
import axiosInstance from '../../conf/axios'
import { useDispatch, useSelector } from 'react-redux'
import { showNotification } from '../Notification/notificationSlice'
import { fetchIndices } from './indicesSlice'
import DeleteIcon from '@mui/icons-material/Delete'
import AttachmentIcon from '@mui/icons-material/Attachment'
import AddIcon from '@mui/icons-material/Add'
import { RootState } from '../../redux/store'

export interface CreateIndexDialogProps {
    maxWidth?: DialogProps['maxWidth']
}

const CreateIndexDialog: FunctionComponent<CreateIndexDialogProps> = ({
    maxWidth,
}) => {
    const availableLanguages = ['en', 'cs']
    const [open, setOpen] = useState(false)
    const [fileName, setFileName] = useState<string | undefined>(undefined)
    const loading = useSelector((state: RootState) => state.indices.loading)

    useEffect(() => {
        if (loading) {
            setOpen(true)
        }
    }, [loading])

    const dispatch = useDispatch()

    const hideDialog = () => {
        if (loading) {
            return
        }
        setOpen(false)
    }

    const showDialog = () => {
        setOpen(true)
    }

    const validationSchema = yup.object().shape({
        name: yup.string().required('Name is required'),
        lowercase: yup.boolean(),
        removeAccentsBeforeStemming: yup.boolean(),
        removePunctuation: yup.boolean(),
        removeStopwords: yup.boolean(),
        useStemmer: yup.boolean(),
        lang: yup.string().required('Language is required'),
        removeAccentsAfterStemming: yup.boolean(),
        file: yup.mixed().notRequired(),
    })

    const formik = useFormik({
        initialValues: {
            name: '',
            lowercase: true,
            removeAccentsBeforeStemming: true,
            removePunctuation: true,
            removeStopwords: true,
            useStemmer: true,
            lang: 'en',
            removeAccentsAfterStemming: true,
            file: undefined,
        },
        validationSchema,
        onSubmit: async (values, { resetForm }) => {
            const jsonBody = {
                name: values.name,
                lowercase: values.lowercase,
                removeAccentsBeforeStemming: values.removeAccentsBeforeStemming,
                removePunctuation: values.removePunctuation,
                removeStopwords: values.removeStopwords,
                useStemmer: values.useStemmer,
                lang: values.lang,
                removeAccentsAfterStemming: values.removeAccentsAfterStemming,
            }
            // const blob = new Blob([JSON.stringify(jsonBody)], {
            //     type: 'application/json',
            // })
            const formData = new FormData()
            formData.append('idxConfig', JSON.stringify(jsonBody))
            if (values.file) {
                formData.append('dataFile', values.file as any)
            }

            let wasSuccessful = false
            try {
                const { data } = await axiosInstance.post(
                    `/indices/${values.name}`,
                    formData,
                    {
                        headers: {
                            'Content-Type': 'multipart/form-docs',
                        },
                    }
                )

                if (data.success) {
                    dispatch(
                        showNotification({
                            message: data.message,
                            severity: 'success',
                            autohideSecs: 5,
                        })
                    )
                    wasSuccessful = true
                } else {
                    dispatch(
                        showNotification({
                            message: data.message,
                            severity: 'error',
                            autohideSecs: 5,
                        })
                    )
                }
            } catch (err: any) {
                dispatch(
                    showNotification({
                        message:
                            'Server is currently unavailable, try again later 😥.',
                        severity: 'error',
                        autohideSecs: 5,
                    })
                )
            }

            // If the request was successful close the dialogclear values
            if (wasSuccessful) {
                hideDialog()
                resetForm()
            }

            // Always fetch new indices
            dispatch(fetchIndices())
        },
    })

    const onLanguageChange = (event: SelectChangeEvent) => {
        formik.setFieldValue('lang', event.target.value)
    }

    const onFileUpload = (event: any) => {
        const file = event.currentTarget.files[0]
        if (file) {
            setFileName(file.name as string)
            formik.setFieldValue('file', file)
        }
    }

    // Method called on closing the dialog
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
                <Button variant="outlined" color="primary" onClick={showDialog}>
                    Create new Index
                </Button>
            </Stack>

            <Dialog
                open={open}
                fullWidth
                onClose={onClose}
                maxWidth={maxWidth || 'lg'}
            >
                <Typography sx={{ ml: 2, mt: 2 }} variant="h5" fontWeight="600">
                    Create New Index
                </Typography>
                <DialogContent>
                    <form onSubmit={formik.handleSubmit}>
                        <TextField
                            fullWidth
                            label="Name"
                            name="name"
                            sx={{ mb: 2 }}
                            value={formik.values.name}
                            onChange={formik.handleChange}
                            error={
                                Boolean(formik.errors.name) &&
                                formik.touched.name
                            }
                            helperText={
                                formik.errors.name &&
                                formik.touched.name &&
                                formik.errors.name
                            }
                        />
                        <FormControl fullWidth sx={{ mb: 2 }}>
                            <InputLabel id="lang-label">Language</InputLabel>
                            <Select
                                fullWidth
                                labelId="lang-label"
                                id="lang"
                                value={formik.values.lang}
                                label="Language"
                                onChange={onLanguageChange}
                            >
                                {availableLanguages.map((lang) => (
                                    <MenuItem key={lang} value={lang}>
                                        {lang}
                                    </MenuItem>
                                ))}
                            </Select>
                        </FormControl>

                        <Typography sx={{ mb: 2 }} variant="h6">
                            Preprocessor Configuration
                        </Typography>
                        <FormGroup>
                            <FormControlLabel
                                control={
                                    <Checkbox
                                        name="lowercase"
                                        value={formik.values.lowercase}
                                        checked={formik.values.lowercase}
                                        onChange={formik.handleChange}
                                    />
                                }
                                label="Lowercase"
                            />
                            <FormControlLabel
                                control={
                                    <Checkbox
                                        name="removeAccentsBeforeStemming"
                                        value={
                                            formik.values
                                                .removeAccentsBeforeStemming
                                        }
                                        checked={
                                            formik.values
                                                .removeAccentsBeforeStemming
                                        }
                                        onChange={formik.handleChange}
                                    />
                                }
                                label="Remove accents before stemming/lemmatization"
                            />
                            <FormControlLabel
                                control={
                                    <Checkbox
                                        name="removePunctuation"
                                        value={formik.values.removePunctuation}
                                        checked={
                                            formik.values.removePunctuation
                                        }
                                        onChange={formik.handleChange}
                                    />
                                }
                                label="Remove punctuation"
                            />
                            <FormControlLabel
                                control={
                                    <Checkbox
                                        name="removeStopwords"
                                        value={formik.values.removeStopwords}
                                        checked={formik.values.removeStopwords}
                                        onChange={formik.handleChange}
                                    />
                                }
                                label="Remove stopwords"
                            />
                            <FormControlLabel
                                control={
                                    <Checkbox
                                        name="useStemmer"
                                        value={formik.values.useStemmer}
                                        checked={formik.values.useStemmer}
                                        onChange={formik.handleChange}
                                    />
                                }
                                label="Use stemmer"
                            />
                            <FormControlLabel
                                control={
                                    <Checkbox
                                        name="removeAccentsAfterStemming"
                                        value={
                                            formik.values
                                                .removeAccentsAfterStemming
                                        }
                                        checked={
                                            formik.values
                                                .removeAccentsAfterStemming
                                        }
                                        onChange={formik.handleChange}
                                    />
                                }
                                label="Remove accents after stemming/lemmatization"
                            />
                        </FormGroup>
                        <Divider sx={{ mt: 1 }} />
                        <Stack sx={{ my: 2 }} direction="column">
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
                                        >
                                            Remove Selection
                                        </Button>
                                    </Stack>
                                </Fragment>
                            )}
                            <Stack></Stack>
                            {!fileName && (
                                <Button
                                    variant="outlined"
                                    color="secondary"
                                    component="label"
                                    // size="small"
                                    startIcon={<AttachmentIcon />}
                                >
                                    Attach JSON Data
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
                        </Stack>
                        <Stack
                            direction="row"
                            justifyContent="flex-end"
                            alignItems="center"
                        >
                            <Button
                                type="submit"
                                variant="contained"
                                disabled={loading}
                                startIcon={<AddIcon />}
                            >
                                Create Index
                            </Button>
                        </Stack>
                    </form>
                </DialogContent>
            </Dialog>
        </Fragment>
    )
}

export default CreateIndexDialog
