import {
    Fragment,
} from 'react'
import { useSelector } from 'react-redux'
import { Virtuoso } from 'react-virtuoso'
import { RootState } from '../../../../redux/store'
import DocumentSearchResult from './DocumentSearchResult'

const Footer = () => {
    return (
        <div
            style={{
                padding: '2rem',
                display: 'flex',
                justifyContent: 'center',
            }}
        >
            Loading...
        </div>
    )
}

const VirtualizedDocumentList = () => {
    const documents = useSelector(
        (state: RootState) => state.indexSearch.documents
    )

    return (
        <Fragment>
            {documents && (
                <Virtuoso
                    style={{ height: '70vh' }}
                    data={documents}
                    // components={{ Footer }}
                    itemContent={(index) => (
                        <DocumentSearchResult document={documents[index]} position={index+1} />
                    )}
                />
            )}
        </Fragment>
    )
}

export default VirtualizedDocumentList
