import com.fasterxml.jackson.module.kotlin.jacksonObjectMapper
import java.io.FileInputStream
import java.io.ObjectInputStream
import java.lang.RuntimeException
import java.nio.file.Paths
import java.util.*


data class Document(
    val text: String?, val id: String?, val title: String?, val date: Date?
)

class Deserializer {

    /**
     * Deserialize a file into a list of documents.
     * @param filename name of the file in resources
     * @param outputFile name of the output file
     */
    fun deserialize(filename: String, outputFile: String) {
        try {
            val file = javaClass.getResource(filename) ?: throw IllegalArgumentException("File $filename not found")
            val objectInputStream = ObjectInputStream(FileInputStream(file.file))

            val javaObject = objectInputStream.readObject()
            objectInputStream.close()
            jacksonObjectMapper().writeValue(Paths.get(outputFile).toFile(), javaObject)
        } catch (ex: RuntimeException) {
            throw IllegalArgumentException(ex.message)
        }
    }
}


fun main() {
    val czechDataName = "TREC/czechData.bin"
    val topicDataName = "TREC/topicData.bin"

    with(Deserializer()) {
        deserialize(czechDataName, "czechData.json")
        deserialize(topicDataName, "topicData.json")
    }
}
