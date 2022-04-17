import { ChangeEvent, Fragment, FunctionComponent, useState } from 'react'
import Dialog, { DialogProps } from '@mui/material/Dialog'
import {
    Button,
    Checkbox,
    DialogContent,
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
import { useDispatch } from 'react-redux'
import { showNotification } from '../Notification/notificationSlice'

export interface CreateIndexDialogProps {
    maxWidth?: DialogProps['maxWidth']
}

interface CreateIndexFields {
    name: string
    lowercase: boolean
    removeAccentsBeforeStemming: boolean
    removePunctuation: boolean
    removeStopwords: boolean
    useStemmer: boolean
    lang: string
    removeAccentsAfterStemming: boolean
    file?: File
}

const CreateIndexDialog: FunctionComponent<CreateIndexDialogProps> = ({
    maxWidth,
}) => {
    const availableLanguages = ['en', 'cs']
    const [open, setOpen] = useState(false)
    const [submitButtonEnabled, setSubmitButtonEnabled] = useState(true)

    const dispatch = useDispatch()

    const hideDialog = () => {
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
        onSubmit: async (values) => {
            setSubmitButtonEnabled(false)
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
            const blob = new Blob([JSON.stringify(jsonBody)], {
                type: 'application/json',
            })
            const formData = new FormData()
            formData.append('json', blob)
            if (values.file) {
                formData.append('file', values.file as any)
            }

            try {
                const { data } = await axiosInstance.post(
                    '/indices',
                    formData,
                    {
                        headers: {
                            'Content-Type': 'multipart/form-data',
                        },
                    }
                )

                if (!data.success) {
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
            setSubmitButtonEnabled(true)
        },
    })

    const onLanguageChange = (event: SelectChangeEvent) => {
        formik.setFieldValue('lang', event.target.value)
    }

    const onFileUpload = (event: any) => {
        formik.setFieldValue('file', event.currentTarget.files[0])
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
                fullWidth={true}
                onClose={hideDialog}
                maxWidth={maxWidth}
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
                        <Stack sx={{ my: 2 }}>
                            <Button
                                variant="contained"
                                color="secondary"
                                component="label"
                            >
                                Attach Documents
                                <input
                                    id="file"
                                    name="file"
                                    type="file"
                                    hidden
                                    onChange={onFileUpload}
                                />
                            </Button>
                        </Stack>
                        <Stack
                            direction="row"
                            justifyContent="flex-end"
                            alignItems="center"
                        >
                            <Button
                                type="submit"
                                variant="contained"
                                disabled={!submitButtonEnabled}
                            >
                                Create
                            </Button>
                        </Stack>
                    </form>
                </DialogContent>
            </Dialog>
        </Fragment>
    )
}

export default CreateIndexDialog
