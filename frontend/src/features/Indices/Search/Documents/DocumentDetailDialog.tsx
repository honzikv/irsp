import {
    Button,
    Dialog,
    DialogContent,
    DialogTitle,
    Divider,
    Paper,
    Stack,
    Typography,
} from '@mui/material'
import { Fragment, FunctionComponent, useState } from 'react'
import { DocumentDto } from '../../indexDtos'
import InfoIcon from '@mui/icons-material/Info'
import { Box } from '@mui/system'
import JSONPretty from 'react-json-pretty'
import 'react-json-pretty/themes/monikai.css'
import DownloadIcon from '@mui/icons-material/Download'

const DocumentDetailDialog: FunctionComponent<DocumentDto> = (props: DocumentDto) => {
    const { id, text, additionalProperties, title } = props
    const [open, setOpen] = useState(false)
    const [downloadButtonDisabled, setDownloadButtonDisabled] = useState(false)

    const onClose = () => {
        setOpen(false)
    }

    const onOpen = () => {
        setOpen(true)
    }

    // Serializes props and saves it to file which the user will be prompted to save
    const downloadAsJson = async () => {
        setDownloadButtonDisabled(true)
        const json = JSON.stringify(props, null, 4)
        const blob = new Blob([json], { type: 'application/json' })
        const href = await URL.createObjectURL(blob)
        const link = document.createElement('a')
        link.href = href
        link.download = `${id}.json`
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
        setDownloadButtonDisabled(false)
    }

    return (
        <Fragment>
            <Button
                onClick={onOpen}
                startIcon={<InfoIcon />}
                variant="contained"
                color="primary"
                size="small"
            >
                Show More
            </Button>
            <Dialog fullWidth maxWidth="lg" open={open} onClose={onClose}>
                <DialogTitle>
                    <Stack
                        direction="row"
                        justifyContent="space-between"
                        alignItems="center"
                        spacing={2}
                    >
                        <Typography variant="body2">
                            ID: "{id}"
                        </Typography>
                        <Button
                            onClick={downloadAsJson}
                            startIcon={<DownloadIcon />}
                            variant="outlined"
                            disabled={downloadButtonDisabled}
                        >
                            Download as JSON
                        </Button>
                    </Stack>
                </DialogTitle>
                <DialogContent>
                    {title && (
                        <Typography
                            variant="h5"
                            fontWeight="bold"
                            sx={{ mt: 2 }}
                        >
                            {title}
                        </Typography>
                    )}

                    <Box
                        sx={{
                            maxHeight: '40vh',
                            overflow: 'auto',
                        }}
                    >
                        <Paper variant="outlined" sx={{px: 2, py: 1}}>
                        {/* <Typography variant="h6">Text</Typography> */}
                        <Typography variant="body1">{text}</Typography>
                        </Paper>
                    </Box>
                    {/* <Divider sx={{ mt: 1 }} /> */}
                    <Typography variant="h6" fontWeight="bold" sx={{ mt: 1, mb: 0, pb: 0 }}>
                        Additional Properties
                    </Typography>
                    <JSONPretty data={additionalProperties} />
                </DialogContent>
            </Dialog>
        </Fragment>
    )
}

export default DocumentDetailDialog
