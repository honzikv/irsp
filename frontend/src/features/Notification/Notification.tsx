import { Alert, AlertColor, Snackbar } from '@mui/material'
import { Fragment, useEffect, useState } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { RootState } from '../../redux/store'
import { consumeNotification } from './notificationSlice'

// Represents notification component that will be displayed on the screen
const Notification = () => {
    const dispatch = useDispatch()
    const notification = useSelector((state: RootState) => state.notification)

    const [displayMessage, setDisplayMessage] = useState('')
    const [open, setOpen] = useState(false)
    const [severity, setSeverity] = useState<AlertColor>('info')
    const [autohideDuration, setAutohideDuration] = useState<number | null>(
        null
    )

    const closeNotification = () => {
        setOpen(false)
        setAutohideDuration(null)
    }

    // Set the message to be displayed if something is set
    useEffect(() => {
        if (notification.message) {
            setDisplayMessage(notification.message)
            setSeverity(notification.severity as AlertColor)
            if (notification.autohideSecs) {
                setAutohideDuration(notification.autohideSecs * 1000)
            }
            // Consume the message from store
            dispatch(consumeNotification())

            // Show the message in the notification
            setOpen(true)
        }
    }, [notification, dispatch])

    return (
        <Fragment>
            <Snackbar
                open={open}
                autoHideDuration={autohideDuration}
                anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
                onClose={() => setAutohideDuration(null)}
            >
                <Alert severity={severity} onClose={closeNotification}>
                    {displayMessage}
                </Alert>
            </Snackbar>
        </Fragment>
    )
}

export default Notification
