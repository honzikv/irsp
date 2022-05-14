import com.fasterxml.jackson.module.kotlin.jacksonObjectMapper
import java.io.File
import java.io.FileInputStream
import java.io.ObjectInputStream
import java.lang.RuntimeException
import java.nio.file.Paths
import java.util.*

class Deserializer {

    /**
     * Deserialize a file into a list of documents.
     * @param filename name of the file in resources
     * @param outputFile name of the output file
     */
    fun deserialize(filename: String, outputFile: String) {
        try {
            val objectInputStream = ObjectInputStream(FileInputStream(File(filename)))
            val javaObject = objectInputStream.readObject()
            objectInputStream.close()
            jacksonObjectMapper().writeValue(Paths.get(outputFile).toFile(), javaObject)
        } catch (ex: RuntimeException) {
            throw IllegalArgumentException(ex.message)
        }
        println("Deserialized file $filename into $outputFile")
    }
}

/**
 * Deserialize .bin java files to .json files that can be used by the python application
 * Arguments:
 *  1st - path to the czechData.bin
 *  2nd - path to the topicData.bin
 */
fun main(args: Array<String>) {
    Deserializer().apply {
        deserialize(args[0], "czechData.json")
        deserialize(args[1], "topicData.json")
    }
}
