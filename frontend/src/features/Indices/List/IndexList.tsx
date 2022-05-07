import { Fragment } from 'react'
import { useSelector } from 'react-redux'
import { RootState } from '../../../redux/store'
import IndexListItem from './IndexListItem'

const IndexList = () => {
    const indices = useSelector((state: RootState) => state.indices.indices)
    return (
        <Fragment>
            {indices && [...indices]
                .sort((a, b) => a.name.localeCompare(b.name))
                .map((index, idx) => (
                    <IndexListItem key={idx} {...index} />
                ))}
        </Fragment>
    )
}

export default IndexList
