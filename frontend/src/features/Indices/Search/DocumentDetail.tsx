import {
    Button,
    Dialog,
    DialogContent,
    DialogTitle,
    Divider,
    Stack,
    Typography,
} from '@mui/material'
import { Fragment, FunctionComponent, useState } from 'react'
import { DocumentDto, DocumentSearchResultDto } from '../indicesDtos'
import InfoIcon from '@mui/icons-material/Info'
import { Box } from '@mui/system'
import JSONPretty from 'react-json-pretty'
import 'react-json-pretty/themes/monikai.css'
import DownloadIcon from '@mui/icons-material/Download'

const DocumentDetail: FunctionComponent<DocumentDto> = (
    props: DocumentDto
) => {
    const { docId, text, additionalProperties } = props
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
        link.download = `${docId}.json`
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
                        <Typography variant="h5">
                            DocumentId: {docId}
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
                    <Typography variant="h4" fontWeight="bold" sx={{ mt: 2 }}>
                        Text
                    </Typography>
                    <Box
                        sx={{
                            // minHeight: '40vh',
                            maxHeight: '40vh',
                            overflow: 'auto',
                        }}
                    >
                        <Typography variant="body1">{text}</Typography>
                    </Box>
                    <Divider sx={{ mt: 1 }} />
                    <Typography variant="h4" fontWeight="bold" sx={{ mt: 2 }}>
                        Additional Properties
                    </Typography>
                    <JSONPretty data={additionalProperties} />
                </DialogContent>
            </Dialog>
        </Fragment>
    )
}

export default DocumentDetail
